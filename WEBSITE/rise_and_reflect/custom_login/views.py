from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')


def profile(request):
    return render(request, 'home/profile.html')


def user_homepage(request):
    return render(request, 'user_home/user-homepage.html')


def set_goals(request):
    return render(request, 'set_goals/set_goals.html')


def profile_summary(request):
    return render(request, 'home/profile_summary.html')

