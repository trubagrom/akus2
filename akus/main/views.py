from django.shortcuts import render
from django.http import HttpResponse


def greet(request):
    return render(request, 'main/greet.html')


def login(request):
    return render(request, 'main/login.html')
