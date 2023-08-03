from django.http import HttpResponse
from django.shortcuts import render
from daily_commitments.models import UserHealthArea
from track_routine.models import RoutineTasks
from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks, TrackedTasks
from django.utils import timezone
from .utils import get_max_order
import re


def create_routine(request, routine_type):
    # TODO: Filter out suggested tasks and don't show custom ones
    if request.POST:
        # turn json into a python dict
        tasks = (request.POST).dict()
        selected_tasks = []
        custom_tasks = []

        user = request.user
        try:
            created_routine = RoutineTasks.objects.filter(user=user, day=timezone.now(), routine_type=routine_type).first()
        except:
            created_routine = False
        if not created_routine:
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
                    if key[:6] == "custom" and key[-4:] != "time" and tasks[key] != "":
                        
                        # Add the task name and duration to custom_tasks list
                        custom_tasks.append([tasks[key], tasks[key + "_time"]])

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
            last_id = PersonalTasks.objects.all().values_list('id', flat=True).order_by('-id').first()

            return render(request, 'tasks/add_tasks.html', {'tasks': area_tasks, 'routine_type': "Morning", "last_id": last_id})

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
        user_ptask = PersonalTasks.objects.get(task_id=task_pk)
        user_ptask.order = idx
        user_ptask.save()
        tasks.append(user_ptask)

    # Same as above to display tasks for a GET request instead of post
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list(
        "duration", "task_id"
    )
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
    if all_user_tasks_list_type == []:
        return render(
            request,
            "tasks/view_tasks.html",
            {
                "create_tasks": "You need to create tasks for the " + routine_type,
            },
        )
    last_id = PersonalTasks.objects.all().values_list('id', flat=True).order_by('-id').first()
    return render(
        request,
        "tasks/edit_tasks.html",
        {
            "tasks": all_user_tasks_list_type,
            "routine_type": routine_type,
            "last_id": last_id
        },
    )

def update_tasks(request, routine_type):
    if request.POST:
        # turn json into a python dict
        tasks = (request.POST).dict()

        user = request.user
        obj = UserProfile.objects.get(user=user)
        area = getattr(obj, "health_area_id")
        health_area = UserHealthArea.objects.get(health_area=area)

        # Get ids and then update personal task with duration and/or name change
        print(tasks)

        for key in tasks:

            if key == "csrfmiddlewaretoken":
                pass
            elif key[:6] != "custom" and key[-4:] == "time" and tasks[key] != "":
                
                print("task_id ", int(re.search("\d+", key)[0]))
                task_id = int(re.search("\d+", key)[0])
                searched_task = Tasks.objects.get(pk=task_id)
                print("This the task I am trying to update 222 ", PersonalTasks.objects.filter(task_id=searched_task))
                if not searched_task:
                    searched_task = Tasks(health_area=health_area, task=tasks[str(task_id)], task_type=routine_type, custom=False)
                    searched_task.save()
                    print("This is where I want to check  ", tasks[key])
                    personal_task = PersonalTasks(user=user, task_id=searched_task, duration=tasks[key], order=get_max_order(user))
                    personal_task.save()
                else:

                    print("searched_task", searched_task)
                    print("Duration ", tasks[key])
                    print("This the task I am trying to update ", PersonalTasks.objects.filter(task_id=searched_task))
                    updated_task = PersonalTasks.objects.filter(task_id=searched_task).update(duration=int(tasks[key]))
                    print(updated_task)
                # updated_task.update(duration=tasks[key])

            elif key[:6] == "custom" and key[-4:] == "time" and tasks[key] != "":

                print(int(re.search("\d+", key)[0]))
                task_id = int(re.search("\d+", key)[0])
                searched_task=Tasks.objects.get(id=task_id)
                print("not searched_task", searched_task)
                
                if not searched_task:
                    searched_task = Tasks(health_area=health_area, task=tasks["custom" + str(task_id)], task_type=routine_type, custom=True)
                    searched_task.save()
                    personal_task = PersonalTasks(user=user, task_id=searched_task, duration=tasks[key], order=get_max_order(user))
                    personal_task.save()
                else:
                    
                    # Add a check to see if personal task exists and if not create that and a tracked task (that uses the routine)
                    updated_personal_task = PersonalTasks.objects.filter(task_id=searched_task).update(duration=tasks[key])
                    updated_task = Tasks.objects.filter(id=task_id).update(task=tasks["custom" + str(task_id)])
                    print(updated_task)
                    # updated_task.update(duration=tasks[key])
                    # updated_task.update(task=tasks["custom" + task_id])


        # # use number on time without custom
        # for key in tasks:
        #     # ignore the csrf token
        #     if key == "csrfmiddlewaretoken":
        #         pass
        #     else:
        #         # if the key is just a number on it's own
        #         try:
        #             personal_task_exists = PersonalTasks.objects.filter(task_id=Tasks.objects.get(id=key))


        return render(
        request,
        "home/index.html",
    )
