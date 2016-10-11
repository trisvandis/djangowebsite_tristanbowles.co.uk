
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    
    )
    
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
    print("Authenticated user = " + str(request.user.is_authenticated()))
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    title = "Login"
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        login(request, user)
        print("Authenticated user = " + str(request.user.is_authenticated()))
        if next:
            return redirect(next)
        return redirect("/")
    context = {
        "form": form,
        "title": title,
        }
        
    return render(request, "accounts_login.html", context)

def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")
    context = {
        "form": form,
        "title": title,
        }
    return render(request, "accounts_register.html", context)
    
def logout_view(request):
    logout(request)
    print("Goodbye")
    print("Authenticated user = " + str(request.user.is_authenticated()))
    return redirect("/")
    
    
    
