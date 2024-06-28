import datetime
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom_login.models import CustomUser
from daily_commitments.views import health_areas
from track_routine.models import RoutineTasks
from tasks.models import PersonalTasks, TrackedTasks, Tasks
from custom_login.models import UserProfile
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout, get_user_model
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt

def index(request):
    return render(request, 'home/index.html')


def profile(request):
    return render(request, 'home/profile.html')


def user_homepage(request):
    return render(request, 'user_home/user-homepage.html')


def set_goals(request):
    return render(request, 'set_goals/set_goals.html')

@login_required(login_url='/accounts/login/')
def profile_summary(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # check to see if a routine for today exists
    try:
        # Get today's date
        today = timezone.now().date()
        routine = RoutineTasks.objects.get(user=user_profile, routine_type="Morning", day=today)
    # Create one if not
    except:
        messages.error(request, "No routine for today found")
        types = ["Morning", "Evening"]
        for routine_type in types:
            routine = RoutineTasks(user=user_profile, routine_type=routine_type)
            routine.save()
            try:
                tracked_tasks = TrackedTasks.objects.get(user=user_profile,
                    personal_task__task_id__task_type=routine_type
                    )
                tracked_tasks.personal_routine=routine
                tracked_tasks.completed=False
                tracked_tasks.save()
            except:
                health_areas(request)

    num_of_total_tasks = TrackedTasks.objects.filter(user=user_profile).count()
    num_of_tasks_complete = TrackedTasks.objects.filter(user=user_profile, date=timezone.now(), completed=True).count()
    if num_of_total_tasks == 0 or num_of_tasks_complete == 0:
        percent_of_all_tasks_completed = 0
    else:
        percent_of_all_tasks_completed = int((num_of_tasks_complete/num_of_total_tasks)*100)

    num_of_eve_tasks = TrackedTasks.objects.filter(user=user_profile, personal_routine__routine_type='Evening').count()
    num_of_eve_complete = TrackedTasks.objects.filter(user=user_profile, date=timezone.now(), completed=True, personal_routine__routine_type='Evening').count()
    if num_of_eve_tasks == 0 or num_of_eve_complete == 0:
        percent_of_eve_tasks_completed = 0
    else:
        percent_of_eve_tasks_completed = int((num_of_eve_complete/num_of_eve_tasks)*100)

    num_of_morn_tasks = TrackedTasks.objects.filter(user=user_profile, personal_routine__routine_type='Morning').count()
    num_of_morn_complete = TrackedTasks.objects.filter(user=user_profile, date=timezone.now(), completed=True, personal_routine__routine_type='Morning').count()
    if num_of_morn_tasks == 0 or num_of_morn_complete == 0:
        percent_of_morn_tasks_completed = 0
    else:
        percent_of_morn_tasks_completed = int((num_of_morn_complete/num_of_morn_tasks)*100)

    return render(request, 'home/profile_summary.html', 
                  {'user_profile': user_profile, 
                   'values': [percent_of_morn_tasks_completed, percent_of_eve_tasks_completed, percent_of_all_tasks_completed]})

@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def delete_account(request):
    user_pk = request.user.pk
    auth_logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).delete()
    return render(request, 'home/index.html')


# Functionality for Android app

def generate_token_or_retrieve_existing_token(user):
    # Check if the user already has an existing token stored
    # If yes, retrieve and return the existing token

    # If the user does not have an existing token, generate a new token
    # You can customize the payload and add any additional claims you need
    payload = {'user_id': user.id, 'username': user.username}
    token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
    user.set_auth_token(token)

    return token

@csrf_exempt
def app_login(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf8'))
        username = json_request['username']
        password = json_request['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            # Generate or retrieve the authentication token
            token = generate_token_or_retrieve_existing_token(user)

            return JsonResponse({"token": token})
        else:
            # Login failed
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

@csrf_exempt
def display_tasks(request):
    if request.method == "POST":
        json_request = json.loads(request.body.decode('utf8'))
        auth_token = json_request['auth_token']

    # Perform authentication and retrieve the username based on the auth_token

        try:
            user = CustomUser.objects.get(auth_token=auth_token)
            username = user.username

            # Return the username as a JSON response
            response_data = {'username': username}
            return JsonResponse(response_data)

        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid authentication token'})

    # Return an error response for any other request method
    return JsonResponse({'error': 'Invalid request'})

