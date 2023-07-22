from datetime import date
from django.shortcuts import render
from .models import RoutineTasks
from tasks.models import PersonalTasks, Tasks


# TODO:
# Return tasks with name, duration, completed, type, custom
# Add checkbox to tell if its completed or not
# Separate evening from morning 
# create new view to handle changing days on page
# 

def track_routine(request):
    # get user
    user = request.user
    # Get user tasks
    # get duration and task_id of the users tasks
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list('id', 'duration', 'task_id')
    # turn it to a list of lists
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

    # for every task of the users
    for task in range(len(all_user_tasks_list)):
        # Get the task with the id
        filtered_task = Tasks.objects.get(id = all_user_tasks_list[task][2])
        # Then add type and task to list
        all_user_tasks_list[task].append(filtered_task.task_type)
        all_user_tasks_list[task].append(filtered_task.task)
        all_user_tasks_list[task].append(filtered_task.custom)
    # filter RoutineTasks for user
    routine = RoutineTasks.objects.filter(user=user)
    # If a routine exists
    if routine:
        # check if routine exists for today
        routine_check = RoutineTasks.objects.filter(day=date.today(), user=user)
        # If it does load that
        if routine_check:
            return render(request, 'routine/track_routine.html', {'routine': routine_check})
    # if it doesn't create one 
    else:
        for task in all_user_tasks_list:
            routine_task = RoutineTasks(personal_task_id=PersonalTasks.objects.get(id=task[0]), user=user)
            routine_task.save()

        routine_today = RoutineTasks.objects.filter(day=date.today(), user=user)

        return render(request, 'routine/track_routine.html', {'routine': routine_today })
        

    return render(request, 'routine/track_routine.html', {'add_tasks': "you need to create tasks"})