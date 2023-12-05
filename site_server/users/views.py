from django.shortcuts import render, HttpResponseRedirect

from django.contrib import auth, messages
from django.urls import reverse

from users.models import  User
from users.forms import UserLoginForm, UserRegistrationForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('comp_vision:index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Вход',
        'form': form }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message='Вы успешно зареганы! Спасибо за ваш пароль)')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm
    context = {
        'title': 'Регистрация',
        'form': form }

    return render(request, 'users/registration.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('comp_vision:index'))