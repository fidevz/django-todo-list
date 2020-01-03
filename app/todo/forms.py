from django.forms import ModelForm
from todo.models import (
    Task
)

class NewTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("title", "content", "priority", "category", "due_date")
