from django.urls import path, include
import todo.views as views

app_name = "todo"

urlpatterns = [
    path('', views.index, name="index"),
    path('account/signup/', views.signup, name="signup"),
    path('complete/', views.complete_task, name="complete_task"),
    path('delete/', views.delete_task, name="delete_task"),
    path('report/', views.report, name="report"),
]
