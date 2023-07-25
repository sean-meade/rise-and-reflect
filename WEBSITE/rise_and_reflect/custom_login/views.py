from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')


def daily_commit(request):
    return render(request, 'daily-commit/daily-commit.html')


def set_goals(request):
    return render(request, 'set_goals/set_goals.html')

