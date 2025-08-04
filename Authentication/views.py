from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user_data_has_error = False

        if not (first_name and last_name and username and email and password and confirm_password):
            messages.error(request, 'All fields are required!')
            user_data_has_error = True

        if User.objects.filter(username=username).exists():
            messages.error(request, 'A user with that username already exists!')
            user_data_has_error = True
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with that email already exists!')
            user_data_has_error = True

        if len(password) < 5:
            messages.error(request, 'Password must be at least 5 characters!')
            user_data_has_error = True
            
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            user_data_has_error = True

        if user_data_has_error:          
            return redirect('register')
        
        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.save()

        messages.success(request, 'Account created successfully, login')
        return redirect('login')

    return render(request, 'Authentication/register.html')

def login_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            messages.error(request, 'All fields are required!')    
            return redirect('login')
        
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)

            # redirect the user to home page
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'Authentication/login.html')

@login_required
def home(request):

    return HttpResponse("You are authenticated<br> <a href='/logout'>Logout</a>")


def logout_user(request):

    logout(request)
    return redirect('login')