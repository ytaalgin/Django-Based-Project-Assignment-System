from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm
from .models import Task
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from .forms import UnavailabilityForm
from .models import Unavailability

@login_required
def create_task(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('task_list')
        else:
            form = TaskForm()
            unavailabilities = Unavailability.objects.all()  # Tüm müsaitlikleri alın
        return render(request, 'tasks/create_task.html', {'form': form, 'unavailabilities': unavailabilities})
    else:
        return redirect('task_list')

@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    unavailability = Unavailability.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'unavailability': unavailability})

@login_required
def upload_document(request, task_id):
    task = get_object_or_404(Task, id=task_id)  # Get the task by ID
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()  # Save the updated task with the uploaded document
            return redirect('task_list')  # Redirect to the task list after upload
    else:
        form = DocumentUploadForm(instance=task)
    return render(request, 'tasks/upload_document.html', {'form': form, 'task': task})


@login_required
def set_unavailability(request):
    if request.method == 'POST':
        form = UnavailabilityForm(request.POST)
        if form.is_valid():
            unavailability = form.save(commit=False)
            unavailability.user = request.user  # Assign the logged-in user
            unavailability.save()
            return redirect('success_page')  # Redirect to a success page or task list
    else:
        form = UnavailabilityForm()
    return render(request, 'tasks/set_unavailability.html', {'form': form})


@login_required
def success_page(request):
    return render(request, 'tasks/success.html')


def home(request):
    return render(request, 'tasks/home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Assuming you have a LoginForm for handling login
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')  # Redirect to task list after login
            else:
                # Handle invalid login
                return render(request, 'tasks/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'tasks/login.html', {'form': form})

