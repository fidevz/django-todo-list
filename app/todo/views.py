from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.db.models import Sum, Count
from datetime import datetime
from django.contrib.auth import login, authenticate

from todo.forms import (
    NewTaskForm
)
from todo.models import (
    Task, Category, Priority
)

@login_required
def index(request):
    if request.method == "POST":
        task_form = NewTaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "New task added!")
            return redirect(reverse('todo:index'))
        else:
            print(task_form.errors)
            messages.error(request, "Invalid data for new task.")

    tasks = Task.objects.filter(user=request.user).select_related('category')

    return render(request, 'todo/index.html', {
        'priorities': Priority.objects.all(),
        'categories': Category.objects.all(),
        'tasks': tasks
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('todo:index')
        else:
            messages.error(request, str(form.errors))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def report(request):
    tasks = Task.objects.filter(user=request.user).select_related('priority')
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    due_missed = tasks.filter(Q(completed=False) \
                            & Q(due_date__lt=datetime.now())).count()
    completed_percentage = round(completed_tasks / max(total_tasks, 1)*100, 2)
    low_tasks = tasks.filter(priority__name="low").count()
    normal_tasks = tasks.filter(priority__name="normal").count()
    high_tasks = tasks.filter(priority__name="high").count()

    return render(request, 'todo/report.html', {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "due_missed": due_missed,
        "completed_percentage": completed_percentage,
        "low_tasks": low_tasks,
        "normal_tasks": normal_tasks,
        "high_tasks": high_tasks,
    })

@login_required
def complete_task(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseBadRequest()
    try:
        task = Task.objects.get(pk=request.POST['task_id'])
        task.completed = request.POST['completed'] == "true"
        task.save()
    except Exception as e:
        return JsonResponse({
            's': 1,
            'm': str(e)
        })
    return JsonResponse({'s':0})

@login_required
def delete_task(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseBadRequest()
    try:
        task = Task.objects.get(pk=request.POST['task_id'])
        task.delete()
    except Exception as e:
        return JsonResponse({
            's': 1,
            'm': str(e)
        })
    return JsonResponse({'s':0})
