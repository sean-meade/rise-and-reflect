from django.shortcuts import render
from .forms import *


def index(request):
    return render(request, 'home/index.html')

<<<<<<< HEAD

def daily_commit(request):
    return render(request, 'daily-commit/daily-commit.html')


def set_goals(request):
    return render(request, 'set_goals/set_goals.html')
=======
>>>>>>> dfffc4f1a2e32ccb73e0bb481c5def3e07492893
