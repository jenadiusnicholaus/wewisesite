from django.shortcuts import render,redirect
from authentication.forms import loginForm, registerForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    form = registerForm()
    return render(request, 'homepage.html', {"form":form})

def user_login(request):
    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # request.session.set_expiry(1200)
                # messages.success(request, f"Welcome again :{username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/login')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login')
    form = loginForm()
    return render(request, 'authentication/signin.html', {'form':form})


def user_logout(request):
    logout(request)
    messages.success(request, f"Logged out successful.")
    return redirect('login')


    