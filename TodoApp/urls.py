from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
]