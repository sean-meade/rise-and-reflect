from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom_login.models import CustomUser
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

    num_of_tasks = TrackedTasks.objects.filter(user=user).count()
    try:
        num_of_tasks_completed_morn = TrackedTasks.objects.filter(user=user, personal_routine=RoutineTasks.objects.get(user=user, routine_type="Morning", day=timezone.now().date() ), completed=True).count()
        num_of_tasks_completed_eve = TrackedTasks.objects.filter(user=user, personal_routine=RoutineTasks.objects.get(user=user, routine_type="Evening", day=timezone.now().date() ), completed=True).count()
    except:
        num_of_tasks_completed_morn = 0
        num_of_tasks_completed_eve = 0
    if num_of_tasks == 0:
        percent_of_tasks_completed_today = 0
    else:
        percent_of_tasks_completed_today = round(((num_of_tasks_completed_morn+num_of_tasks_completed_eve)/num_of_tasks) * 100)

    # Get number of Personal tasks that have a Task with custom=False
    # How many of them are completed = True
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "task_id"
    )
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]
    goal_tasks_completed = 0
    total_goal_tasks = 0
    for task in all_user_tasks_list:
        
        query_task = Tasks.objects.get(id=task[0])
        if query_task.custom == False:
            total_goal_tasks+=1
            task_type = query_task.task_type

            try:
                if TrackedTasks.objects.get(user=user, personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=task[0])), completed=True, personal_routine=RoutineTasks.objects.get(day=timezone.now().date(),routine_type=task_type )):
                    goal_tasks_completed+=1
            except:
                pass

    if total_goal_tasks == 0:
        percent_of_goal_tasks_completed = 0
    else:
        percent_of_goal_tasks_completed = round((goal_tasks_completed/total_goal_tasks) * 100)

    return render(request, 'home/profile_summary.html', 
                  {'user_profile': user_profile, 
                   'values': [percent_of_goal_tasks_completed, percent_of_tasks_completed_today, 37]})

@login_required(login_url='/accounts/login/')
@require_http_methods(['POST'])
def delete_account(request):
    user_pk = request.user.pk
    auth_logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).delete()
    return render(request, 'home/index.html')


# Functionality for app

def generate_token_or_retrieve_existing_token(user):
    # Check if the user already has an existing token stored
    # If yes, retrieve and return the existing token

    # If the user does not have an existing token, generate a new token
    # You can customize the payload and add any additional claims you need
    payload = {'user_id': user.id, 'username': user.username}
    token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
    user.set_auth_token(token)

    # Save the token in the database or user model
    print("user.auth_token", user.auth_token)

    return token

@csrf_exempt
def app_login(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode('utf8'))
        username = json_request['username']
        password = json_request['password']
        print("username", username)
        print("password", password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        print("user.username", user.username)

        if user is not None:
            # Login successful
            # Generate or retrieve the authentication token
            token = generate_token_or_retrieve_existing_token(user)

            print("token", str(JsonResponse({"token": token})))

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

