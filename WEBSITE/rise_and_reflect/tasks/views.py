import operator
from django.shortcuts import render
from daily_commitments.forms import CommitmentsForm
from daily_commitments.models import UserHealthArea
from rise_and_reflect import settings
from track_routine.models import RoutineTasks
from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks, TrackedTasks
from django.utils import timezone
from .utils import get_max_order, rename_keys
import re
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def create_tasks(request, routine_type, task_post=True):
    # Get user and health area
    user = UserProfile.objects.get(user=request.user)
    area = getattr(user, "health_area_id")
    health_area = UserHealthArea.objects.get(health_area=area)

    # fill in values if they are there
    # get all tasks for health area and routine_type and display them
    tasks_tuple = PersonalTasks.objects.filter(user=user, task_id__health_area=area, 
                                                        task_id__task_type=routine_type).values(
            "task_id__id", "task_id__task", "task_id__task_type", "duration", 
        )
        
    if len(tasks_tuple) > 0:
        tasks_list = rename_keys(list(tasks_tuple))
    else:
        # get all tasks for health area and routine_type and display them
        tasks_tuple = Tasks.objects.filter(health_area=area, task_type=routine_type).values(
                    "id", "task", "task_type", "custom"
                )
        tasks_list = tasks_tuple

    if request.POST and task_post == True:
        # check to see if a routine for today exists
        try:
            # Get today's date
            today = timezone.now().date()
            routine = RoutineTasks.objects.get(user=user, routine_type=routine_type, day=today)
        # Create one if not
        except Exception as error:
            print("No routine for today found: ", error)
            routine = RoutineTasks(user=user, routine_type=routine_type)
            routine.save()

        # get the json from request payload
        tasks = (request.POST).dict()

        # Get a list of all the users Task ids
        users_routine_type_task_ids = set(PersonalTasks.objects.filter(user=user, 
                                                                       task_id__task_type=routine_type).values_list(
                                                                           "task_id__id", flat=True))

        # Create an empty set to house the task ids coming from the form
        ids_coming_in = set()

        # For everything in the payload
        for key in tasks:
            # ignore the csrf token
            if key == "csrfmiddlewaretoken":
                pass
            # add the id to set
            else:
                try:
                    ids_coming_in.add(int(re.search("\d+", key)[0]))
                except:
                    pass
                
        # Edit these tasks:
        edit_these_tasks = list(ids_coming_in.intersection(users_routine_type_task_ids))

        for task_to_edit in edit_these_tasks:
            current_task = Tasks.objects.get(id=task_to_edit, task_type=routine_type)
            custom = getattr(current_task, "custom")
            # update time and name if custom task
            if custom:
                if tasks["custom" + str(task_to_edit) + "_time"] == '' or tasks["custom" + str(task_to_edit)] == '':
                    current_task.delete()
                else:
                    PersonalTasks.objects.filter(task_id=task_to_edit).update(duration=tasks["custom" + str(task_to_edit) + "_time"])
                    Tasks.objects.filter(id=task_to_edit).update(task=tasks["custom" + str(task_to_edit)])
            # Update time if suggested
            else:
                if tasks[str(task_to_edit) + "_time"] != '':
                    PersonalTasks.objects.filter(task_id=task_to_edit).update(duration=tasks[str(task_to_edit) + "_time"])
                else:
                    delete_ptask = PersonalTasks.objects.get(task_id = task_to_edit)
                    delete_ptask.delete()
        
        # Add these tasks:
        add_these_tasks = ids_coming_in - users_routine_type_task_ids
        for task_to_add in add_these_tasks:
            # If custom create task and get time user wants to do it
            if "custom" + str(task_to_add) in tasks:
                task_obj = Tasks(
                    health_area=health_area,
                    task=tasks["custom" + str(task_to_add)],
                    task_type=routine_type,
                    custom=True)
                task_obj.save()
                task_time = tasks["custom" + str(task_to_add) + "_time"]
            # if suggested the get the task and time
            else:
                task_obj = Tasks.objects.get(id=task_to_add)
                task_time = tasks[str(task_to_add) + "_time"]
            
            if task_time != '':
                try:
                    ptask_exists = PersonalTasks.objects.get(user=user,
                                                             task_id=task_obj)
                    ptask_exists.delete()
                except Exception as e:
                    print("No Personal task were found: ", e) 
            
                # Then create a personal task 
                personal_task = PersonalTasks(
                                            user=user,
                                            task_id=task_obj,
                                            duration=task_time)
                personal_task.save()
                # Create a tracked task
                tracked_task = TrackedTasks(
                    user=user,
                    personal_task=personal_task,
                    personal_routine=routine
                )
                tracked_task.save()

        # Delete these:
        delete_these_tasks = users_routine_type_task_ids - ids_coming_in
        for task_to_delete in delete_these_tasks:
            # If custom delete the Task and it will cascade
            if "custom" + str(task_to_delete) in tasks:
                delete_ptask = PersonalTasks.objects.get(task_id = task_to_delete)
                delete_ptask.delete()
            # If suggested delete Personal and it will cascade
            else:
                delete_ptask = PersonalTasks.objects.get(task_id = task_to_delete)
                delete_ptask.delete()

        if routine_type == "Evening":
            routine_type = "Morning"
            # TODO: Test if the next 5 lines are needed
            tasks_tuple = PersonalTasks.objects.filter(user=user, task_id__health_area=area, 
                                                          task_id__task_type=routine_type).values(
                "task_id__id", "task_id__task", "task_id__task_type", "duration", "task_id__custom" 
            )
            tasks_list = rename_keys(list(tasks_tuple))
            # fill in values if they are there
            try:
                # get all tasks for health area and routine_type and display them
                tasks_tuple = PersonalTasks.objects.filter(user=user, task_id__health_area=area, 
                                                                task_id__task_type=routine_type).values(
                        "task_id__id", "task_id__task", "task_id__task_type", "duration", "task_id__custom" 
                    )
                    
                if len(tasks_tuple) > 0:
                    tasks_list = rename_keys(list(tasks_tuple))
                else:
                    # get all tasks for health area and routine_type and display them
                    tasks_tuple = Tasks.objects.filter(health_area=area, task_type=routine_type).values(
                                "id", "task", "task_type", "custom"
                            )
                    tasks_list = list(tasks_tuple)
            except Exception as e:
                print("No personal tasks found: ", e)

            # Get the latest Task id for creating custom tasks in html
            last_id = Tasks.objects.all().values_list('id', flat=True).order_by('-id').first()

            if last_id == None:
                last_id = 0
            
            return render(
                request,
                "tasks/edit_tasks.html",
                {
                    "tasks": tasks_list, 'routine_type': routine_type, "last_id": last_id
                },
            )
        else:
            ptasks = PersonalTasks.objects.filter(user=user, task_id__task_type=routine_type).values(
                "task_id__id", "task_id__task", "task_id__task_type", "duration", 
            )
            return render(request, 'routine/order_tasks.html', {'tasks': rename_keys(ptasks), "routine_type": routine_type})

    # Get the latest Task id for creating custom tasks in html
    last_id = Tasks.objects.all().values_list('id', flat=True).order_by('-id').first()
    if last_id == None:
        last_id = 0
    return render(
        request,
        "tasks/edit_tasks.html",
        {
            "tasks": list(tasks_list),'routine_type': routine_type, "last_id": last_id
        },
    )

def order_tasks(request, routine_type):
    user = UserProfile.objects.get(user=request.user)
    ptasks = PersonalTasks.objects.filter(user=user, task_id__task_type=routine_type).values(
                "task_id__id", "task_id__task", "task_id__task_type", "duration", 
            )
    return render(request, 'routine/order_tasks.html', {'tasks': rename_keys(ptasks), "routine_type": routine_type})

def sort(request, routine_type):
    user = UserProfile.objects.get(user=request.user)
    tasks_pks_order = request.POST.getlist('task_order')
    tasks = []
    for idx, task_pk in enumerate(tasks_pks_order, start=1):
        user_ptask = PersonalTasks.objects.get(task_id=task_pk)
        user_ptask.order = idx
        user_ptask.save()
        tasks.append(user_ptask)

    ptasks = PersonalTasks.objects.filter(user=user, task_id__task_type=routine_type).values(
                "task_id__id", "task_id__task", "task_id__task_type", "duration", 
            )

    if len(ptasks) <= 0:
            return render(
        request,
        "routine/order_tasks.html",
        {
            "create_tasks": "You need to create tasks",
        },
    )

    return render(request, 'partials/order_tasks_partial.html', {'tasks': rename_keys(ptasks), "routine_type": routine_type})

def edit_all_tasks(request, routine_type):
    user = UserProfile.objects.get(user=request.user)

    # get all tasks for health area and routine_type and display them
    tasks_tuple = PersonalTasks.objects.filter(user=user, task_id__task_type= routine_type).values(
            "task_id__id", "task_id__task", "task_id__task_type", "duration", "task_id__custom"
        )
        
    if len(tasks_tuple) > 0:
        if request.POST:
            # check to see if a routine for today exists
            try:
                # Get today's date
                today = timezone.now().date()
                routine = RoutineTasks.objects.get(user=user, routine_type=routine_type, day=today)
            # Create one if not
            except Exception as error:
                print("No routine for today found: ", error)
                routine = RoutineTasks(user=user, routine_type=routine_type)
                routine.save()

            # get the json from request payload
            tasks = (request.POST).dict()

            # Get a list of all the users Task ids
            users_routine_type_task_ids = set(PersonalTasks.objects.filter(user=user, 
                                                                       task_id__task_type=routine_type).values_list(
                                                                           "task_id__id", flat=True))

            # Create an empty set to house the task ids coming from the form
            ids_coming_in = set()

            # For everything in the payload
            for key in tasks:
                # ignore the csrf token
                if key == "csrfmiddlewaretoken":
                    pass
                # add the id to set
                else:
                    try:
                        ids_coming_in.add(int(re.search("\d+", key)[0]))
                    except:
                        pass
                    
            # Edit these tasks:
            edit_these_tasks = list(ids_coming_in.intersection(users_routine_type_task_ids))

            for task_to_edit in edit_these_tasks:
                current_task = Tasks.objects.get(id=task_to_edit, task_type=routine_type)
                custom = getattr(current_task, "custom")
                # update time and name if custom task
                if custom:
                    if tasks["custom" + str(task_to_edit) + "_time"] == '' or tasks["custom" + str(task_to_edit)] == '':
                        current_task.delete()
                    else:
                        PersonalTasks.objects.filter(task_id=task_to_edit).update(duration=tasks["custom" + str(task_to_edit) + "_time"])
                        Tasks.objects.filter(id=task_to_edit).update(task=tasks["custom" + str(task_to_edit)])
                # Update time if suggested
                else:
                    if tasks[str(task_to_edit) + "_time"] != '':
                        PersonalTasks.objects.filter(task_id=task_to_edit).update(duration=tasks[str(task_to_edit) + "_time"])
                    else:
                        delete_ptask = PersonalTasks.objects.get(task_id = task_to_edit)
                        delete_ptask.delete()
            
            # Add these tasks:
            add_these_tasks = ids_coming_in - users_routine_type_task_ids
            for task_to_add in add_these_tasks:
                # If custom create task and get time user wants to do it
                if "custom" + str(task_to_add) in tasks:
                    task_obj = Tasks(
                        health_area=user.health_area,
                        task=tasks["custom" + str(task_to_add)],
                        task_type=routine_type,
                        custom=True)
                    task_obj.save()
                    task_time = tasks["custom" + str(task_to_add) + "_time"]
                # if suggested the get the task and time
                else:
                    task_obj = Tasks.objects.get(id=task_to_add)
                    task_time = tasks[str(task_to_add) + "_time"]
                
                if task_time != '':
                    try:
                        ptask_exists = PersonalTasks.objects.get(user=user,
                                                                task_id=task_obj)
                        ptask_exists.delete()
                    except Exception as e:
                        print("No Personal task were found: ", e) 
                
                    # Then create a personal task 
                    personal_task = PersonalTasks(
                                                user=user,
                                                task_id=task_obj,
                                                duration=task_time)
                    personal_task.save()
                    # Create a tracked task
                    tracked_task = TrackedTasks(
                        user=user,
                        personal_task=personal_task,
                        personal_routine=routine
                    )
                    tracked_task.save()

            # Delete these:
            delete_these_tasks = users_routine_type_task_ids - ids_coming_in
            for task_to_delete in delete_these_tasks:
                # If custom delete the Task and it will cascade
                if "custom" + str(task_to_delete) in tasks:
                    delete_ptask = Tasks.objects.get(id = task_to_delete)
                    delete_ptask.delete()
                # If suggested delete Personal and it will cascade
                else:
                    try:
                        delete_ptask = PersonalTasks.objects.get(task_id__id = task_to_delete)
                        delete_ptask.delete()
                    except Exception as e:
                        print("No PersonalTask created from Task")
        tasks_tuple = PersonalTasks.objects.filter(user=user, task_id__task_type= routine_type).values(
            "task_id__id", "task_id__task", "task_id__task_type", "duration", "task_id__custom"
        )
        tasks_list = rename_keys(list(tasks_tuple))
    else:
        tasks_list = "Please create tasks first"

    # Get the latest Task id for creating custom tasks in html
    last_id = PersonalTasks.objects.filter(user=user, task_id__task_type= routine_type).values_list(
        'id', flat=True).order_by('-id').first()

    if last_id == None:
        last_id = 0
    
    return render(
        request,
        "tasks/edit_all_tasks.html",
        {
            "tasks": tasks_list, "last_id": last_id, "routine_type": routine_type
        },
    )
            
