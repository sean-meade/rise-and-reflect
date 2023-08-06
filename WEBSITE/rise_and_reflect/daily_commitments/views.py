from django.shortcuts import redirect, render

from tasks.models import PersonalTasks
from .forms import CommitmentsForm
from .models import HEALTH_AREAS, UserHealthArea, UserTimeCommitments
from tasks.models import Tasks
from custom_login.models import UserProfile
from django.contrib.auth.decorators import login_required


# @login_required(login_url='/accounts/login/')
# def get_commitments(request):

#     users_commitments = UserTimeCommitments.objects.get(user=request.user)
#     if users_commitments:
#         form = CommitmentsForm(initial={
#             "hours_of_sleep": getattr(users_commitments, "hours_of_sleep"),
#             "work_time_from": getattr(users_commitments, "work_time_from"),
#             "work_time_to": getattr(users_commitments, "work_time_to"),
#             "commute_time": getattr(users_commitments, "commute_time"),
#             "wake_time": getattr(users_commitments, "wake_time"),
#             "get_ready_time": getattr(users_commitments, "get_ready_time"),
#         })
#         if getattr(users_commitments, "wake_time") == None:
#             wake_time=False
#         else:
#             wake_time=True
#     else:
#         form = CommitmentsForm
#     return render(request, 'daily-commit/daily-commit.html', {'form': form, 'wake_time': wake_time})

@login_required(login_url='/accounts/login/')
def daily_commit(request):

    if request.POST:
        # grab data from form
        form = CommitmentsForm(request.POST)
        # If the form submitted by user is valid
        if form.is_valid():
            # Save that info (but don't commit yet)
            commitments = form.save(commit=False)
            # Add the user
            commitments.user = request.user
            # then save
            commitments.save()

        obj = UserProfile.objects.get(user=request.user)
        area = getattr(obj, "health_area_id")
        routine_type = "Evening"
        # Grab the tasks related to the health area
        area_tasks = Tasks.objects.filter(health_area=area, custom=False, task_type=routine_type)
        last_id = PersonalTasks.objects.all().values_list('id', flat=True).order_by('-id').first()
        if last_id == None:
            last_id = 0

        # Same as above to display tasks for a GET request instead of post
        all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
            "duration", "task_id"
        )
        all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]
        all_user_task_ids_list = [y[1] for y in all_user_tasks_list]

        all_user_tasks_list_type = {"Suggested": [], "Custom": []}

        obj = UserProfile.objects.get(user=request.user)
        area = getattr(obj, "health_area_id")
        all_suggested_tasks_tuple = Tasks.objects.filter(health_area=area, custom=False, task_type=routine_type).values_list(
            "id"
        )
        all_suggested_tasks_list = [list(k) for k in all_suggested_tasks_tuple]

        for suggested_task in range(len(all_suggested_tasks_list)):
            if all_suggested_tasks_list[suggested_task][0] not in all_user_task_ids_list:
                
                filtered_suggested_task = Tasks.objects.get(id=all_suggested_tasks_list[suggested_task][0], task_type=routine_type)

                current_task = []
                current_task.append("No time given")
                current_task.append(all_suggested_tasks_list[suggested_task][0])
    
                current_task.append(filtered_suggested_task.task_type)
                current_task.append(filtered_suggested_task.task)
                current_task.append(filtered_suggested_task.custom)
                all_user_tasks_list_type["Suggested"].append(current_task)


        for task in range(len(all_user_tasks_list)):
            try:
                filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][1], task_type=routine_type)
                current_task = []
                current_task.append(all_user_tasks_list[task][0])
                current_task.append(all_user_tasks_list[task][1])
                current_task.append(filtered_task.task_type)
                current_task.append(filtered_task.task)
                current_task.append(filtered_task.custom)
                if filtered_task.custom == True:
                    all_user_tasks_list_type["Custom"].append(current_task)
                else:
                    all_user_tasks_list_type["Suggested"].append(current_task)
            except Exception as error:
                print("Error :", error)
        # send tasks to page for user to choose what to add
        return render(request, 'tasks/edit_tasks.html', {'tasks': all_user_tasks_list_type, 'routine_type': "Evening", "last_id": last_id})

    try:
        users_commitments = UserTimeCommitments.objects.get(user=request.user)
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

@login_required(login_url='/accounts/login/')
def health_areas(request):
    # When user presses a button to choose health area
    if request.POST:
        # grab the health area
        area = request.POST['area']

        # Get the user profile of the user
        user_profile = UserProfile.objects.get(user=request.user)
        user_health_area = getattr(user_profile, "health_area")
        all_suggested_tasks = Tasks.objects.filter(health_area=user_health_area, custom=False).values_list("id")
        if user_profile.health_area:
            for task in all_suggested_tasks:
                try:
                    PersonalTasks.objects.filter(user=request.user, task_id=Tasks.objects.get(id=task[0])).delete()
                except:
                    pass
        # Add health area
        user_profile.health_area=UserHealthArea(health_area=area)
        user_profile.save()
        try:
            users_commitments = UserTimeCommitments.objects.get(user=request.user)
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
