from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
    return render(request, 'todo/home.html')

def signup_user(request):
    message = None
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2 :
            try:
                user = User.objects.create_user(username, password= password1)
            except IntegrityError:
                message = f"Sorry username {username} already exists"
            else:
                user.save()
                login(request, user)
                return redirect('homepage')
        else:
            # if password and reenter password doesnot match
            message = "Password & Password confirmation doesn't match"

    return render(request, 'todo/signup.html', {'form' : UserCreationForm(), 'message': message})

def login_user(request):
    form = AuthenticationForm()
    message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            message = "username/password doesnot match"
            
    return render(request, 'todo/login.html', {'form': form, 'message': message})

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')

@login_required
def current_todos(request):
    todos = Todo.objects.filter(user= request.user, datecompleted__isnull= True).order_by('-created')
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def create_todo(request):
    form = TodoForm()
    message = None
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_form = form.save(commit = False)
        except ValueError:
            message = "inputs given were wrong"
        else:
            new_form.user = request.user
            new_form.save()
            return redirect('current_todos')

    return render(request, 'todo/createtodo.html', {'form': form, 'message': message})

@login_required
def view_todo(request, todo_id):
    instance = get_object_or_404(Todo, pk= todo_id, user= request.user)
    message = None
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance= instance)
            form.save()
        except ValueError:
            message = "inputs given were wrong"
        else:
            return redirect('current_todos')

    form = TodoForm(instance= instance)
    return render(request, 'todo/viewtodo.html', {'instance' : instance, 'form' : form, 'message': message})

@login_required
def completed_todo(request, todo_id):
    if request.method == 'POST':
        instance = get_object_or_404(Todo, pk= todo_id, user= request.user)
        instance.datecompleted = timezone.now()
        instance.save()
        return redirect('current_todos')

@login_required
def delete_todo(request, todo_id):
    if request.method == "POST":
        instance = get_object_or_404(Todo, pk= todo_id, user= request.user)
        instance.delete()
        return redirect('current_todos')

@login_required
def completed_todos(request):
    message = None
    try:
        todos = Todo.objects.filter(user= request.user, datecompleted__isnull= False).order_by('-datecompleted')
    except Exception:
        todos = None
    return render(request, 'todo/mycompletedtodos.html', {'todos':todos})

@login_required
def unfinish_todo(request, todo_id):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk= todo_id, user= request.user, datecompleted__isnull= False)
        todo.datecompleted = None
        todo.save()
        return redirect('completed_todos')

@login_required
def delete_todo_completed(request, todo_id):
    if request.method == "POST":
        instance = get_object_or_404(Todo, pk= todo_id, user= request.user)
        instance.delete()
        return redirect('completed_todos')