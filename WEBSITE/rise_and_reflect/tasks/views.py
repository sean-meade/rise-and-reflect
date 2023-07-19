import json
from django.shortcuts import redirect, render

from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks
from daily_commitments.models import UserHealthArea
from daily_commitments.views import health_goals

def create_routine(request):
    if request.POST:
        
        # turn json into a python dict
        tasks = (request.POST).dict()
        selected_tasks = []
        custom_tasks = []
        # go through dict
        for key in tasks:
            # ignore the csrf token
            if key == 'csrfmiddlewaretoken':
                pass
            else:
                # if the key is just a number on it's own
                try: 
                    int(key)
                    # it is an existing task and the user has selected it so add it selected_tasks
                    selected_tasks.append([key,tasks[key + "_time"] ])
                # If it is a custom one
                except:
                    if key[:6] == 'custom' and key[-4:] != 'time' and tasks[key] != '':
                        # Add the task name and duration to custom_tasks list
                        custom_tasks.append([tasks[key],tasks[key + "_time"] ])

        print(custom_tasks)
        # Add the custom tasks to the database based on the inputs from the user
        for task_name, duration in custom_tasks:
            print(task_name)

            # Get the health area for the user
            # TODO: might be worth adding 'Custom' to the list of areas
            user_profile_obj = UserProfile.objects.get(user=request.user)
            print("Hello", user_profile_obj)
            # user_health_area_val = getattr(user_profile_obj, 'user_health_area')
            # obj = UserHealthArea.objects.get(health_area=user_health_area_val)
            # health_area = getattr(obj, 'health_area')
            # Create the task
            this_task = Tasks(health_area=user_profile_obj.health_area, task=task_name, task_type="Evening")
            this_task.save()
            # add the id and duration of this newly create task to the selected_tasks list
            selected_tasks.append([this_task.id, duration])

        
        for task in selected_tasks:
            personal_task = PersonalTasks(
                task_id = Tasks.objects.get(id=task[0]),
                duration = task[1],
                user=request.user)
            personal_task.save()

        # TODO: Redirect to page that displays a users tasks
        return render(request, 'tasks/view_tasks.html', {'tasks': selected_tasks})