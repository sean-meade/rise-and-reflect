from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from track_routine.models import RoutineTasks
from tasks.models import PersonalTasks, TrackedTasks, Tasks
from custom_login.models import UserProfile
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout, get_user_model
from django.utils import timezone

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

    num_of_tasks = PersonalTasks.objects.filter(user=user).count()
    num_of_tasks_completed_morn = TrackedTasks.objects.filter(user=user, personal_routine=RoutineTasks.objects.get(user=user, routine_type="Morning", day=timezone.now().date() ), completed=True).count()
    num_of_tasks_completed_eve = TrackedTasks.objects.filter(user=user, personal_routine=RoutineTasks.objects.get(user=user, routine_type="Evening", day=timezone.now().date() ), completed=True).count()
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
        print(task[0])
        print(timezone.now().date())
        print(Tasks.objects.get(id=task[0]))
        
        query_task = Tasks.objects.get(id=task[0])
        if query_task.custom == False:
            total_goal_tasks+=1
            task_type = query_task.task_type
            print(TrackedTasks.objects.filter(user=user, personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=task[0])), completed=True, personal_routine=RoutineTasks.objects.get(day=timezone.now().date(),routine_type=task_type )))

            try:
                if TrackedTasks.objects.get(user=user, personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=task[0])), completed=True, personal_routine=RoutineTasks.objects.get(day=timezone.now().date(),routine_type=task_type )):
                    goal_tasks_completed+=1
            except:
                pass
    print(goal_tasks_completed)
    print(total_goal_tasks)

    if total_goal_tasks == 0:
        percent_of_goal_tasks_completed = 0
    else:
        percent_of_goal_tasks_completed = round((goal_tasks_completed/total_goal_tasks) * 100)
    print(percent_of_goal_tasks_completed)

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