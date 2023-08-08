from django.shortcuts import render
from daily_commitments.forms import CommitmentsForm
from daily_commitments.models import UserHealthArea
from track_routine.models import RoutineTasks
from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks, TrackedTasks
from django.utils import timezone
from .utils import get_max_order
import re
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def create_routine(request, routine_type, evening=False):
    print("SEAN - DIZ IS DEE WAY", evening)
    # Get user and health area
    user = request.user
    obj = UserProfile.objects.get(user=user)
    area = getattr(obj, "health_area_id")
    health_area = UserHealthArea.objects.get(health_area=area)
    custom_area = UserHealthArea.objects.get(health_area='None')

    # Post goes up top
    if request.POST and evening==False:
        # check to see if a routine for today exists
        try:
            routine = RoutineTasks.objects.get(user=user, routine_type=routine_type)
        # Create one if not
        except Exception as error:
            print("error: ", error)
            routine = RoutineTasks(user=user, routine_type=routine_type)
            routine.save()

        # get the json from request payload
        tasks = (request.POST).dict()

        # Get a list of all the users Task ids
        all_users_task_ids = set(PersonalTasks.objects.filter(user=request.user).values_list("task_id", flat=True))

        # Create an empty set you house the task ids for evening/morning
        users_routine_type_task_ids = set()
        # For all task ids
        for task_id in all_users_task_ids:
            # Add it to set if the task id has the right routine_type
            try:
                ptask = Tasks.objects.get(id=task_id, task_type=routine_type)
                users_routine_type_task_ids.add(task_id)
            except:
                pass

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
                    delete_ptask = PersonalTasks.objects.get(task_id = task_to_edit)
                    tracked_task_to_delete = TrackedTasks.objects.get(personal_task=delete_ptask)
                    tracked_task_to_delete.delete()
                    delete_task = Tasks.objects.get(id=task_to_edit)
                    delete_task.delete()
                else:
                    PersonalTasks.objects.filter(task_id=task_to_edit).update(duration=tasks["custom" + str(task_to_edit) + "_time"])
                    Tasks.objects.filter(id=task_to_edit).update(task=tasks["custom" + str(task_to_edit)])
            # Update time if suggested
            else:
                if tasks[str(task_to_edit) + "_time"] != '':
                    PersonalTasks.objects.filter(task_id=task_to_edit).update(duration=tasks[str(task_to_edit) + "_time"])
                else:
                    try:
                        delete_ptask = PersonalTasks.objects.get(task_id = task_to_edit)
                        tracked_task_to_delete = TrackedTasks.objects.get(personal_task=delete_ptask)
                        tracked_task_to_delete.delete()
                        delete_ptask.delete()
                    except:
                        pass
        
        # Add these tasks:
        add_these_tasks = ids_coming_in - users_routine_type_task_ids
        for task_to_add in add_these_tasks:
            # If custom create task and get time user wants to do it
            if "custom" + str(task_to_add) in tasks:
                task_obj = Tasks(
                    health_area=custom_area,
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
                tracked_task_to_delete = TrackedTasks.objects.get(personal_task=delete_ptask)
                tracked_task_to_delete.delete()
                delete_task = Tasks.objects.get(id=task_to_delete)
                delete_task.delete()
            # If suggested delete Personal and it will cascade
            else:
                delete_ptask = PersonalTasks.objects.get(task_id = task_to_delete)
                tracked_task_to_delete = TrackedTasks.objects.get(personal_task=delete_ptask)
                tracked_task_to_delete.delete()
                delete_ptask.delete()
        if routine_type == "Morning":
            all_user_tasks = {"Morning": [], "Evening": []}
            # For all task ids
            for task_id in all_users_task_ids:
                task = {}
                # Add it to set if the task id has the right routine_type
                try:
                    this_task = Tasks.objects.get(id=task_id, task_type="Morning")
                    task_name = getattr(this_task, "task")
                    task_id = getattr(this_task, "id")
                    task["name"] = task_name
                    task["id"] = task_id
                    this_ptask = PersonalTasks.objects.get(user=request.user, task_id=this_task)
                    task_time = getattr(this_ptask, "duration")
                    task["time"] = task_time
                    all_user_tasks["Morning"].append(task)
                except:
                    try:
                        this_task = Tasks.objects.get(id=task_id, task_type="Evening")
                        task_name = getattr(this_task, "task")
                        task_id = getattr(this_task, "id")
                        task["name"] = task_name
                        task["id"] = task_id
                        this_ptask = PersonalTasks.objects.get(task_id=this_task)
                        task_time = getattr(this_ptask, "duration")
                        task["time"] = task_time
                        all_user_tasks["Evening"].append(task)
                    except:
                        pass
            
            return render(request, 'routine/edit_routine.html', {'tasks': all_user_tasks})

    if not evening:
        routine_type = "Morning"
    
    # get all tasks for health area and routine_type and display them
    all_suggested_tasks_tuple = Tasks.objects.filter(health_area=area, custom=False, task_type=routine_type).values_list(
                "id", "task", "task_type"
            )
    
    # Create dict to send to html
    all_user_tasks_list_type = {"Suggested": [], "Custom": []}

    # For suggested task create its own dict
    for stask in all_suggested_tasks_tuple:
        current_task = {}
        current_task["name"] = stask[1]
        current_task["type"] = stask[2]
        current_task["id"] = stask[0]

        try:
            ptask = PersonalTasks.objects.get(task_id=Tasks.objects.get(id=stask[0]))
            task_duration = getattr(ptask, "duration")
        except:
            task_duration = "No time given"
        
        current_task["duration"] = task_duration
        #  add it to suggested
        all_user_tasks_list_type["Suggested"].append(current_task)
    
    # Get all personal tasks for user
    all_user_personal_tasks = PersonalTasks.objects.filter(user=request.user).values_list(
                "task_id", "duration"
            )

    # Check to see which ones are custom tasks
    for ctask in all_user_personal_tasks:
        try:
            custom_task = Tasks.objects.get(id=ctask[0], custom=True, task_type=routine_type)
            task_name = getattr(custom_task, "task")
            task_type = getattr(custom_task, "task_type")
            task_id = ctask[0]
            current_task = {
                "name": task_name,
                "type": task_type,
                "id": task_id,
                "duration": ctask[1]
            }
            # Add it to the custom list
            all_user_tasks_list_type["Custom"].append(current_task)
        except Exception as error:
            print("Here is the Error: ", error)

    # Get the latest Task id for creating custom tasks in html
    last_id = Tasks.objects.all().values_list('id', flat=True).order_by('-id').first()
    if last_id == None:
        last_id = 0
    print("HELLO SEAN, THIS IS BEING CAUGHT", all_user_tasks_list_type)
    return render(
        request,
        "tasks/edit_tasks.html",
        {
            "tasks": all_user_tasks_list_type,'routine_type': routine_type, "last_id": last_id
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

    all_user_tasks = {"Morning": [], "Evening": []}

    all_users_task_ids = set(PersonalTasks.objects.filter(user=request.user).values_list("task_id", flat=True))
    # For all task ids
    for task_id in all_users_task_ids:
        task = {}
        # Add it to set if the task id has the right routine_type
        try:
            this_task = Tasks.objects.get(id=task_id, task_type="Morning")
            task_name = getattr(this_task, "task")
            task_id = getattr(this_task, "id")
            task["name"] = task_name
            task["id"] = task_id
            this_ptask = PersonalTasks.objects.get(task_id=this_task)
            task_time = getattr(this_ptask, "duration")
            task["time"] = task_time
            all_user_tasks["Morning"].append(task)
        except:
            this_task = Tasks.objects.get(id=task_id, task_type="Evening")
            task_name = getattr(this_task, "task")
            task_id = getattr(this_task, "id")
            task["name"] = task_name
            task["id"] = task_id
            this_ptask = PersonalTasks.objects.get(task_id=this_task)
            task_time = getattr(this_ptask, "duration")
            task["time"] = task_time
            all_user_tasks["Evening"].append(task)

    if all_user_tasks == []:
            return render(
        request,
        "routine/edit_routine.html",
        {
            "create_tasks": "You need to create tasks",
        },
    )

    return render(request, 'partials/order_tasks.html', {'tasks': all_user_tasks})
