from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, MyUserCreationForm, ChangeUserProfile
from .models import Todo, UserProfile
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import user_not_logged_in
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def home_page(request):
    return render(request, 'todo/home.html')

@user_not_logged_in
def sign_up_user(request):
    message = None
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2 :
            try:
                form = MyUserCreationForm(request.POST)
                if not form.is_valid():
                    raise IntegrityError()
            except IntegrityError:
                message = f"Sorry username or email already exists"
            else:
                form.save()
                messages.success(request, f'account successfully created for {username}')
                return redirect('login')
        else:
            # if password and reenter password doesnot match
            message = "Password & Password confirmation doesn't match"
    context = {
        'form' : MyUserCreationForm(),
        'message' : message,
    }

    return render(request, 'todo/signup.html', context)

@user_not_logged_in
def sign_in_user(request):
    form = AuthenticationForm()
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            error_message = "username/password doesnot match"

    context = {
        'form': form, 
        'error_message': error_message
    }
            
    return render(request, 'todo/signin.html', context)

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')

@login_required
def current_todos(request):
    todos = Todo.objects.filter(user= request.user, datecompleted__isnull= True).order_by('-created')
    context = {
        'todos': todos
    }
    return render(request, 'todo/currenttodos.html', context)

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

    context = {
        'form': form, 
        'message': message
    }

    return render(request, 'todo/createtodo.html', context)

@login_required
def view_todo(request, todo_id):
    instance = get_object_or_404(Todo, pk= todo_id, user= request.user)
    error_message = None
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance= instance)
            form.save()
        except ValueError:
            error_message = "inputs given were wrong"
        else:
            messages.success(request, 'todo saved')
            
    form = TodoForm(instance= instance)
    context ={
        'instance' : instance, 
        'form' : form, 
        'error_message': error_message
    }

    return render(request, 'todo/viewtodo.html', context)

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
    
    context = {
        'todos':todos,
    }
    return render(request, 'todo/mycompletedtodos.html', context)

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

@login_required
def profile(request):
    message = None
    userprofile = UserProfile.objects.get(user= request.user)
    if request.method == 'POST':
        form = ChangeUserProfile(request.POST, request.FILES, instance= userprofile)
        if form.is_valid():
            form.save()
            message = 'profile picture updated'

    form = ChangeUserProfile(instance= userprofile)
    total_todos = Todo.objects.filter(user= request.user).count()
    pending_todos = Todo.objects.filter(user= request.user, datecompleted__isnull= True).count()
    completed_todos = Todo.objects.filter(user= request.user, datecompleted__isnull= False).count()
    
    context = {
        'total_todos' : total_todos,
        'pending_todos' : pending_todos,
        'completed_todos' : completed_todos,
        'form' : form,
        'message' : message,
    }

    return render(request, 'todo/profile.html', context)

@login_required
def change_password(request):
    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(data= request.POST, user= request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            message = 'password changed successfully'
        else:
            message = 'password change failed'

    form = PasswordChangeForm(user= request.user)
    context = {
        'form' : form,
        'message' : message,
    }
    return render(request, 'todo/change_password.html', context)