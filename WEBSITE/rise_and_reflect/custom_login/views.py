from django.shortcuts import render
from .forms import *

def index(request):
    return render(request, 'home/index.html')
