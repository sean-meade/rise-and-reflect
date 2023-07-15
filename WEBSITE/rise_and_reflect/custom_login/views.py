from django.shortcuts import redirect, render
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile

def index(request):
    return render(request, 'home/index.html')

