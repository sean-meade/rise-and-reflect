from django.shortcuts import render
from .forms import *

def index(request):
    return render(request, 'home/index.html')


def profile(request):
    return render(request, 'profile.html')


def user_homepage(request):
    return render(request, 'user-homepage.html')

