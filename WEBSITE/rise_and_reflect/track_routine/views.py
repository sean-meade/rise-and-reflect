from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from custom_login.models import UserProfile
from daily_commitments.models import UserTimeCommitments
from .models import RoutineTasks
from tasks.models import PersonalTasks, Tasks, TrackedTasks
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def display_routine(request):

    user = UserProfile.objects.get(user=request.user)

    try:
        # Get task, type (from Tasks) order,duration, task_id (PersonalTasks)
        personal_tasks = PersonalTasks.objects.filter(user=user).values(
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
        list_of_commits = UserTimeCommitments.objects.get(user=user).__dict__
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
            commitments['bed_time'] = (wake_time_fix - timedelta(hours=int(hours_of_sleep))).time()

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
    except:
        messages.error(request, "You need to create a routine first")
        return render(request, 'routine/display_routine.html', {'message': 'Please craete Routine in order to view it'})

# create new view to handle changing days on page
@login_required(login_url='/accounts/login/')
def track_routine(request):
    user = UserProfile.objects.get(user=request.user)
    
    tracked_tasks = TrackedTasks.objects.filter(user=user).values_list(
                                    "personal_task__task_id__task", 
                                    "personal_task__task_id__task_type",
                                    "personal_task__duration",
                                    "completed")
    
    if len(tracked_tasks) == 0:
        all_user_tasks_tuple = PersonalTasks.objects.filter(user=user).values('id', 'task_id', 'task_id__task_type')
        
        for task in all_user_tasks_tuple:
            ptask = PersonalTasks.objects.get(id=task['id'])
            user_routine = RoutineTasks.objects.get(user=user, routine_type=task['task_id__task_type'])
            tracked_task = TrackedTasks(personal_task=ptask, 
                                        personal_routine=user_routine, 
                                        user=user)
            tracked_task.save()

    tracked_tasks = TrackedTasks.objects.filter(user=user).values(
                                    "id",
                                    "personal_task__task_id__task", 
                                    "personal_task__task_id__task_type",
                                    "personal_task__duration",
                                    "completed")
    return render(
        request, "routine/track_routine.html", {"routine": list(tracked_tasks)}
    )

def edit_track_routine(request):
    user = UserProfile.objects.get(user=request.user)
    
    if request.POST:
        tracked_tasks = TrackedTasks.objects.filter(user=user).values(
                                    "id",
                                    "personal_task__task_id__task", 
                                    "personal_task__task_id__task_type",
                                    "personal_task__duration",
                                    "completed")

        # get the json from request payload
        tasks = [int(item) for item in list((request.POST).dict().values()) if item.isdigit()]

        for task in list(tracked_tasks):
            if task["completed"] == False and task["id"] in tasks:
                t = TrackedTasks.objects.get(id=task["id"])
                t.completed = True
                t.save()
            else:
                t = TrackedTasks.objects.get(id=task["id"])
                t.completed = False
                t.save()
    tracked_tasks = TrackedTasks.objects.filter(user=user).values(
                                    "id",
                                    "personal_task__task_id__task", 
                                    "personal_task__task_id__task_type",
                                    "personal_task__duration",
                                    "completed")
    
    return render(
        request, "routine/track_routine.html", {"routine": list(tracked_tasks)}
    )
