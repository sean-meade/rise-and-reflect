from django.shortcuts import render
from .forms import *

def index(request):
    return render(request, 'home/index.html')

def daily_commit(request):
    return render(request, 'daily-commit/daily-commit.html')

