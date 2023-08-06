from datetime import datetime, timedelta
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from daily_commitments.models import UserTimeCommitments
from .models import RoutineTasks
from tasks.models import PersonalTasks, Tasks, TrackedTasks
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def display_routine(request):

    # Get task, type (from Tasks) order,duration, task_id (PersonalTasks)
    personal_tasks = PersonalTasks.objects.filter(user=request.user).values(
        "task_id", "duration", "order"
    )

    morn_tasks = []

    eve_tasks = []

    for ptask in personal_tasks:
        t = Tasks.objects.get(id=ptask['task_id'])
        if t.task_type == "Morning":
            morn_tasks.append({
                'task_id': ptask['task_id'],
                'task': t.task,
                'duration': ptask['duration'],
                'order': ptask['order'],
            })
        elif t.task_type == "Evening":
            eve_tasks.append({
                'task_id': ptask['task_id'],
                'task': t.task,
                'duration': ptask['duration'],
                'order': ptask['order'],
            })

    # Get hours of sleep
    list_of_commits = UserTimeCommitments.objects.get(user=request.user).__dict__
    hours_of_sleep = list_of_commits["hours_of_sleep"]

    commitments ={}
    commitments['hours_of_sleep'] = hours_of_sleep

    # Get either wake time or work commitments
    wake_time = list_of_commits["wake_time"]
    if wake_time != None:
        commitments['wake_time'] = wake_time
        
    # for wake time:
        # Eve
        # wake time + 5 mins = start time
        wake_time_fix = datetime.strptime(str(wake_time), '%H:%M:%S')
        commitments['bed_time'] = wake_time_fix - timedelta(hours=int(hours_of_sleep))

        morn_start_time = wake_time_fix + timedelta(minutes=5)
        # start time = time of first task
        morn_tasks[0]['start_time'] = morn_start_time.time()
        duration = int(morn_tasks[0]['duration'])

        for morn_task in morn_tasks[1:]:
       
            # time of 1st + duration (change to mins) = time of second
            morn_start_time = morn_start_time + timedelta(minutes=duration)
            morn_task['start_time'] = morn_start_time.time()
            duration = int(morn_task['duration'])
            
            # continue
        # Morn
        # wake time - sleep hours = bed time
        eve_start_time = wake_time_fix - timedelta(hours=hours_of_sleep)

        for eve_task in reversed(eve_tasks):
            duration = int(eve_task['duration'])
            eve_start_time = eve_start_time - timedelta(minutes=duration)
            eve_task['start_time'] = eve_start_time.time()
                    
    else:
        
    # for work commits
        work_time_from = list_of_commits["work_time_from"]
        work_time_to = list_of_commits["work_time_to"]
        commute_time = list_of_commits["commute_time"]
        get_ready_time = list_of_commits["get_ready_time"]

        # time start work - duration to get ready for work = time to get ready
        work_time_from_fix = datetime.strptime(str(work_time_from), '%H:%M:%S')
        get_ready_start = work_time_from_fix - timedelta(minutes=get_ready_time)
        commitments['get_ready_start'] = get_ready_start.time()
        commitments['get_ready_time'] = get_ready_time
        commitments['work_time_from'] = work_time_from

        # Create datetime objects for each time (a and b)
        dateTimeA = datetime.strptime(str(work_time_to), '%H:%M:%S') 
        dateTimeB = datetime.strptime(str(work_time_from), '%H:%M:%S') 
        # Get the difference between datetimes (as timedelta)
        dateTimeDifference = dateTimeA - dateTimeB
        # Divide difference in seconds by number of seconds in hour (3600)  
        dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600

        commitments['work_hours'] = dateTimeDifferenceInHours
        # time to get ready - duration of last morn task = start time of last morn task
        morn_start_time = get_ready_start
        for morn_task in reversed(morn_tasks):
            duration = int(morn_task['duration'])
            morn_start_time = morn_start_time - timedelta(minutes=duration)
            morn_task['start_time'] = morn_start_time.time()
        # start time of last morn task - duration of second last morn task = start time of second last morn task
        # continue for all morn tasks
        # time of first morn task - 15mins = wake time
        wake_time = morn_start_time - timedelta(minutes=5)
        commitments['wake_time'] = wake_time.time()
        # wake time - hours of sleep = bed time
        bed_time_fix = wake_time - timedelta(hours=int(hours_of_sleep))
        
        commitments['bed_time'] = bed_time_fix.time()

        eve_start_time = bed_time_fix

        for eve_task in reversed(eve_tasks):
            duration = int(eve_task['duration'])
            eve_start_time = eve_start_time - timedelta(minutes=duration)
            eve_task['start_time'] = eve_start_time.time()
        
        # bed time - duration of last eve task = start time of last eve task
        # start time of last eve task - duration of second last eve task = start time of second last eve task
        # continue
    return render(request, 'routine/display_routine.html', {'morn_tasks':morn_tasks, 'eve_tasks': eve_tasks, 'commitments': commitments})

# TODO:
# Separate evening from morning
# create new view to handle changing days on page
@login_required(login_url='/accounts/login/')
def track_routine(request):

    # get user
    user = request.user
    # Get user tasks
    # get duration and task_id of the users tasks
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "id", "duration", "task_id"
    )
    # turn it to a list of lists
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

    if request.POST:
        # list of tasks that are ticked
        tasks = [int(item) for item in list((request.POST).dict().values()) if item.isdigit()]
        # List of all tasks of user
        all_user_tasks_ids = [item[2] for item in all_user_tasks_list ]

        # Run through all the users personal tasks
        for count, task in enumerate(all_user_tasks_ids):
            # check to see is that task is ticked
            if task in tasks:
                # set that task to true
                TrackedTasks.objects.filter(personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=task), user=user)).update(completed=True)
            else:
                # Set that task to false
                TrackedTasks.objects.filter(personal_task=PersonalTasks.objects.get(task_id=Tasks.objects.get(id=all_user_tasks_ids[count]), user=user)).update(completed=False)

    # for every task of the users
    for task in range(len(all_user_tasks_list)):
        # Get the task with the id
        filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][2])
        # Then add type and task to list
        all_user_tasks_list[task].append(filtered_task.task_type)
        all_user_tasks_list[task].append(filtered_task.task_type)
        all_user_tasks_list[task].append(filtered_task.task)
        all_user_tasks_list[task].append(filtered_task.custom)
    # filter RoutineTasks for user to check if a routine exists
    routine = RoutineTasks.objects.filter(user=user)
    

    # If a routine exists
    if routine:
        try:
            # check if routine exists for today
            routine_check = RoutineTasks.objects.filter(day=timezone.now(), user=user, routine_type="Morning").first()
            
            if routine_check == None:
                routine_check = RoutineTasks(user=user, routine_type="Morning")
                routine_check.save()

        # If it is a custom one
        except:
            routine_check = RoutineTasks(user=user, routine_type="Morning")
            routine_check.save()

        # get duration and task_id of the users tasks
        all_user_tasks_tuple = PersonalTasks.objects.filter(
            user=request.user
        ).values_list("duration", "task_id")
        # turn it to a list of lists
        all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]
        

        # for every task of the users
        for task in range(len(all_user_tasks_list)):
            # Get the task using the id
            filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][1])
            # Then add type and task to list
            all_user_tasks_list[task].append(filtered_task.task_type)
            all_user_tasks_list[task].append(filtered_task.task)
            all_user_tasks_list[task].append(filtered_task.custom)

            filter_by_this_task = PersonalTasks.objects.get(task_id = filtered_task, user=request.user)
            try:
                tracked_task = TrackedTasks.objects.get(personal_task = filter_by_this_task,  personal_routine=routine_check)
            except:
                tracked_task = TrackedTasks(personal_task=filter_by_this_task, personal_routine=routine_check, user=request.user)
                tracked_task.save()
            
            all_user_tasks_list[task].append(tracked_task.completed)

        if routine_check:
            return render(
                request, "routine/track_routine.html", {"routine": all_user_tasks_list}
            )

    return render(
        request, "routine/track_routine.html", {"add_tasks": "you need to create tasks and/or go to Create Routine."}
    )

