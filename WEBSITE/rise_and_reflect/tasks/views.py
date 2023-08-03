from django.http import HttpResponse
from django.shortcuts import render
from track_routine.models import RoutineTasks
from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks, TrackedTasks
from django.utils import timezone
from .utils import get_max_order


def create_routine(request, routine_type):
    print("routine_type", routine_type)
    # TODO: Filter out suggested tasks and don't show custom ones
    if request.POST:
        # turn json into a python dict
        tasks = (request.POST).dict()
        selected_tasks = []
        custom_tasks = []

        user = request.user
        print(tasks)
        try:
            created_routine = RoutineTasks.objects.filter(user=user, day=timezone.now(), routine_type=routine_type).first()
            print(created_routine.routine_type)
        except:
            created_routine = False
        if not created_routine:
            # Create user routine
            created_routine = RoutineTasks(user=user, routine_type=routine_type)
            print("2",created_routine)
            created_routine.save()
        # go through dict
        for key in tasks:
            # ignore the csrf token
            if key == "csrfmiddlewaretoken":
                pass
            else:
                # if the key is just a number on it's own
                try:
                    print("here")
                    int(key)
                    print("there")
                    # it is an existing task and the user has selected it so add it selected_tasks
                    selected_tasks.append([key, tasks[key + "_time"]])
                    print("selected_tasks ", selected_tasks)
                    # TODO: Check to see if a Personal task exists with task_id
                    personal_task_exists = PersonalTasks.objects.filter(task_id=Tasks.objects.get(id=key))
                    # Create the personal task
                    if not personal_task_exists:
                        this_personal_task = PersonalTasks(
                            user=user,
                            task_id=Tasks.objects.get(id=key),
                            duration=tasks[key + "_time"],
                            order=get_max_order(user)
                        )
                        this_personal_task.save()
                        this_trackable_task = TrackedTasks(personal_task=this_personal_task, personal_routine=created_routine)
                        this_trackable_task.save()
                # If it is a custom one
                except:
                    print("hit")
                    if key[:6] == "custom" and key[-4:] != "time" and tasks[key] != "":
                        
                        # Add the task name and duration to custom_tasks list
                        custom_tasks.append([tasks[key], tasks[key + "_time"]])
                        print("custom_tasks ",custom_tasks)

        # Get the health area for the user
        user_profile_obj = UserProfile.objects.get(user=request.user)
        # Add the custom tasks to the database based on the inputs from the user
        for task_name, duration in custom_tasks:
            custom_task_exists = Tasks.objects.filter(task=task_name, task_type=routine_type)
            if not custom_task_exists:
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
                    order=get_max_order(user),
                    task_id=this_task,
                    duration=duration,
                    user=user,
                )
                this_personal_task.save()
                # this_personal_task.user.set([user])
                this_trackable_task = TrackedTasks(personal_task=this_personal_task, personal_routine=created_routine)
                this_trackable_task.save()

        if routine_type == "Evening":
            obj = UserProfile.objects.get(user=request.user)
            area = getattr(obj, "health_area_id")
            area_tasks = Tasks.objects.filter(health_area=area, task_type="Morning")

            return render(request, 'tasks/add_tasks.html', {'tasks': area_tasks, 'routine_type': "Morning"})

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
        return render(request, "routine/edit_routine.html",
        {
            "tasks": all_user_tasks_list,
        },)

    # Same as above to display tasks for a GET request instead of post
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "duration", "task_id"
    )
    print("tuple", all_user_tasks_tuple)
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
        "routine/edit_routine.html",
        {
            "create_tasks": "You need to create tasks for the " + routine_type,
        },
    )

    print("tasks", all_user_tasks_list)
    return render(
        request,
        "routine/edit_routine.html",
        {
            "tasks": all_user_tasks_list,
        },
    )

def sort(request):
    tasks_pks_order = request.POST.getlist('task_order')
    tasks = []
    for idx, task_pk in enumerate(tasks_pks_order, start=1):
        print(idx, task_pk)
        user_ptask = PersonalTasks.objects.get(task_id=task_pk)
        user_ptask.order = idx
        user_ptask.save()
        tasks.append(user_ptask)

    # Same as above to display tasks for a GET request instead of post
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "duration", "task_id"
    )
    print("tuple", all_user_tasks_tuple)
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

    
    for task in range(len(all_user_tasks_list)):
        try:
            filtered_task = Tasks.objects.get(id=all_user_tasks_list[task][1])
            all_user_tasks_list[task].append(filtered_task.task_type)
            all_user_tasks_list[task].append(filtered_task.task)
            all_user_tasks_list[task].append(filtered_task.custom)
        except:
            return render(
        request,
        "routine/edit_routine.html",
        {
            "create_tasks": "You need to create tasks for the " + routine_type,
        },
    )

    return render(request, 'partials/order_tasks.html', {'tasks': all_user_tasks_list})

def edit_tasks(request, routine_type):
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