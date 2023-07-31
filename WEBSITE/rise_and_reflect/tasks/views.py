from django.shortcuts import render
from track_routine.models import RoutineTasks
from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks, TrackedTasks

def create_routine(request, routine_type):

def set_evening_tasks(request):
    return render(request, 'tasks/set_tasks_evening.html')


def set_morning_tasks(request):
    return render(request, 'tasks/set_tasks_morning.html')


    # TODO: Filter out suggested tasks and don't show custom ones
    if request.POST:
        # turn json into a python dict
        tasks = (request.POST).dict()
        selected_tasks = []
        custom_tasks = []

        user = request.user

        # Create user routine
        created_routine = RoutineTasks(user=user, routine_type=routine_type)
        created_routine.save()
        # go through dict
        for key in tasks:
            # ignore the csrf token
            if key == "csrfmiddlewaretoken":
                pass
            else:
                # if the key is just a number on it's own
                try:
                    int(key)
                    # it is an existing task and the user has selected it so add it selected_tasks
                    selected_tasks.append([key, tasks[key + "_time"]])
                    # Create the personal task
                    this_personal_task = PersonalTasks(
                        user=user,
                        task_id=Tasks.objects.get(id=key),
                        duration=tasks[key + "_time"],
                    )
                    this_personal_task.save()
                    this_trackable_task = TrackedTasks(personal_task=this_personal_task, personal_routine=created_routine)
                    this_trackable_task.save()
                # If it is a custom one
                except:
                    if key[:6] == "custom" and key[-4:] != "time" and tasks[key] != "":
                        # Add the task name and duration to custom_tasks list
                        custom_tasks.append([tasks[key], tasks[key + "_time"]])
        
        if routine_type == "Evening":
            obj = UserProfile.objects.get(user=request.user)
            print("obj", obj)
            print(obj.health_area)
            area = getattr(obj, "health_area_id")
            area_tasks = Tasks.objects.filter(health_area=area, task_type="Morning")
            return render(request, 'tasks/add_tasks.html', {'tasks': area_tasks, 'routine_type': "Morning"})

        # Get the health area for the user
        user_profile_obj = UserProfile.objects.get(user=request.user)
        # Add the custom tasks to the database based on the inputs from the user
        for task_name, duration in custom_tasks:
            # Create the task
            this_task = Tasks(
                health_area=user_profile_obj.health_area,
                task=task_name,
                task_type=routine_type,
                custom=True,
            )
            this_task.save()
            # Create the personal task
            this_personal_task = PersonalTasks(
                user=user,
                task_id=this_task,
                duration=duration,
            )
            this_personal_task.save()
            this_trackable_task = TrackedTasks(personal_task=this_personal_task, personal_routine=created_routine)
            this_trackable_task.save()

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

        # return all the users tasks
        return render(request, "tasks/view_tasks.html",
        {
            "tasks": all_user_tasks_list,
        },)

    # Same as above to display tasks for a GET request instead of post
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "duration", "task_id"
    )
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

    
    for task in range(len(all_user_tasks_list)):
        try:
            filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][1], task_type=routine_type)
            all_user_tasks_list[task].append(filtered_task.task_type)
            all_user_tasks_list[task].append(filtered_task.task)
            all_user_tasks_list[task].append(filtered_task.custom)
        except:
            return render(
        request,
        "tasks/view_tasks.html",
        {
            "create_tasks": "You need to create tasks for the " + routine_type,
        },
    )

    return render(
        request,
        "tasks/view_tasks.html",
        {
            "tasks": all_user_tasks_list,
        },
    )
