from django.shortcuts import render, redirect
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')


def user_logout(request):
    logout(request)
    return redirect('index')
