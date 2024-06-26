from django.shortcuts import render
from tasks.views import create_tasks
from tasks.models import PersonalTasks
from .forms import CommitmentsForm
from .models import HEALTH_AREAS, UserHealthArea, UserTimeCommitments
from tasks.models import Tasks
from custom_login.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def daily_commit(request):

    user = UserProfile.objects.get(user=request.user)

    if request.POST:
        # grab data from form
        form = CommitmentsForm(request.POST)
        # If the form submitted by user is valid
        if form.is_valid():
            # Save that info (but don't commit yet)
            commitments = form.save(commit=False)
            # Add the user
            commitments.user = user
            # then save
            commitments.save()
            
        return create_tasks(request, routine_type="Evening", task_post=False)
    
     # Get the user profile of the user
    user_profile = UserProfile.objects.get(user=user)
    user_health_area = getattr(user_profile, "health_area")
    # Add health area
    user_profile.health_area=UserHealthArea(health_area=user_health_area)
    user_profile.save()
    try:
        users_commitments = UserTimeCommitments.objects.get(user=user)
        if users_commitments:
            form = CommitmentsForm(initial={
                "hours_of_sleep": getattr(users_commitments, "hours_of_sleep"),
                "work_time_from": getattr(users_commitments, "work_time_from"),
                "work_time_to": getattr(users_commitments, "work_time_to"),
                "commute_time": getattr(users_commitments, "commute_time"),
                "wake_time": getattr(users_commitments, "wake_time"),
                "get_ready_time": getattr(users_commitments, "get_ready_time"),
            })
            if getattr(users_commitments, "wake_time") == None:
                wake_time=False
            else:
                wake_time=True
    except:
        form = CommitmentsForm
        wake_time=True

    return render(request, 'daily-commit/daily-commit.html', {'form': form, 'wake_time': wake_time})

@login_required(login_url='/accounts/login/')
def health_areas(request):
    user = UserProfile.objects.get(user=request.user)
    # When user presses a button to choose health area
    if request.POST:
        # grab the health area
        area = request.POST['area']

        # Get the user profile of the user
        user_profile = UserProfile.objects.get(user=user)
        user_health_area = getattr(user_profile, "health_area")
        all_suggested_tasks = Tasks.objects.filter(health_area=user_health_area, custom=False).values_list("id")
        if user_profile.health_area:
            for task in all_suggested_tasks:
                try:
                    PersonalTasks.objects.filter(user=user, task_id=Tasks.objects.get(id=task[0])).delete()
                except:
                    pass
        # Add health area
        user_profile.health_area=UserHealthArea(health_area=area)
        user_profile.save()
        try:
            users_commitments = UserTimeCommitments.objects.get(user=user)
            if users_commitments:
                form = CommitmentsForm(initial={
                    "hours_of_sleep": getattr(users_commitments, "hours_of_sleep"),
                    "work_time_from": getattr(users_commitments, "work_time_from"),
                    "work_time_to": getattr(users_commitments, "work_time_to"),
                    "commute_time": getattr(users_commitments, "commute_time"),
                    "wake_time": getattr(users_commitments, "wake_time"),
                    "get_ready_time": getattr(users_commitments, "get_ready_time"),
                })
                if getattr(users_commitments, "wake_time") == None:
                    wake_time=False
                else:
                    wake_time=True
        except:
            form = CommitmentsForm
            wake_time=True
        # Take user to the page where they can choose their health area
        return render(request, 'daily-commit/daily-commit.html', {'form': form, 'wake_time': wake_time})
    # On GET request send data to create health area buttons
    return render(request, 'daily-commit/health-area.html', {'areas': HEALTH_AREAS})
