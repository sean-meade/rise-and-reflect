import json
from django.shortcuts import redirect, render
from .models import Tasks, UserRoutine
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
                    print(int(key))
                    int(key)
                    # it is an existing task and the user has selected it so add it selected_tasks
                    selected_tasks.append([key,tasks[key + "_time"] ])
                # If it is a custom one
                except:
                    print(key[-4:])
                    if key[:6] == 'custom' and key[-4:] != 'time':
                        # Add the task name and duration to custom_tasks list
                        custom_tasks.append([tasks[key],tasks[key + "_time"] ])

        # Add the custom tasks to the database based on the inputs from the user
        for task_name, duration in custom_tasks:

            # Get the health area for the user
            # TODO: might be worth adding 'Custom' to the list of areas
            obj = UserHealthArea.objects.get(user=request.user)
            health_area = getattr(obj, 'health_area')
            # Create the task
            # TODO: make the task_type dynamic
            this_task = Tasks(user=request.user, health_area=obj, task=task_name, task_type="Evening")
            this_task.save()
            # add the id and duration of this newly create task to the selected_tasks list
            selected_tasks.append([this_task.id, duration])

        
        for task_id, duration_of_task in selected_tasks:
            routine = UserRoutine(user=request.user, )
        
        return redirect(health_goals)