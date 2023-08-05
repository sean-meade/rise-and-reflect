from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom_login.models import UserProfile
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout, get_user_model

def index(request):
    return render(request, 'home/index.html')


def profile(request):
    return render(request, 'home/profile.html')


def user_homepage(request):
    return render(request, 'user_home/user-homepage.html')


def set_goals(request):
    return render(request, 'set_goals/set_goals.html')


def profile_summary(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'home/profile_summary.html', {'user_profile': user_profile})

@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def delete_account(request):
    user_pk = request.user.pk
    auth_logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).delete()
    return render(request, 'home/index.html')