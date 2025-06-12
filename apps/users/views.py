from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,f'Hi {request.user.username}! What will we watch today?')
            return redirect(reverse('home'))
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method=='POST':
        username=request.POST["username"]
        email=request.POST.get("email")
        password=request.POST["password1"]
        conf_password=request.POST["password2"]
        if password!=conf_password:
            messages.error(request,"Passwords don't match")
            return render(request, 'register.html')
        
        user=User.objects.create_user(username=username,
                                          email=email,
                                          password=password,
                                          )
        user.save()
        messages.success(request,'Registration is successful. Yaaaay')
        return redirect(reverse('login'))
        


    return render(request, 'register.html')