# tasks/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import create_task, task_list, upload_document, login_view, set_unavailability, success_page, home

urlpatterns = [
    path('', home, name='home'),  # This will be the homepage
    path('create/', create_task, name='create_task'),
    path('tasks', task_list, name='task_list'),
    path('upload/<int:task_id>/', upload_document, name='upload_document'),
    path('', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', login_view, name='login'),  # Add this line for login
    path('set-unavailability/', set_unavailability, name='set_unavailability'),
    path('success/', success_page, name='success_page'),  # Add this line
]

