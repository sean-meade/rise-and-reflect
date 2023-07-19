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
                    int(key)
                    # it is an existing task and the user has selected it so add it selected_tasks
                    selected_tasks.append([key,tasks[key + "_time"] ])
                # If it is a custom one
                except:
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

        create_routine_vals = []

        # for x in range(len(selected_tasks)):
        #     name = "task_id_" + (x + 1)
        #     value = selected_tasks[x]
        #     create_routine_vals.append([name, value])

        y = 8 - len(selected_tasks)

        for i in range(y):
            selected_tasks.append([None, None])

        routine = UserRoutine(user=request.user,
                              task_id_1=Tasks.objects.get(id=selected_tasks[0][0]),
                              duration_1=selected_tasks[0][1],
                              task_id_2=Tasks.objects.get(id=selected_tasks[1][0]),
                              duration_2=selected_tasks[1][1],
                              task_id_3=Tasks.objects.get(id=selected_tasks[2][0]),
                              duration_3=selected_tasks[2][1],
                              task_id_4=Tasks.objects.get(id=selected_tasks[3][0]),
                              duration_4=selected_tasks[3][1],
                              task_id_5=Tasks.objects.get(id=selected_tasks[4][0]),
                              duration_5=selected_tasks[4][1],
                              task_id_6=Tasks.objects.get(id=selected_tasks[5][0]),
                              duration_6=selected_tasks[5][1],
                              task_id_7=Tasks.objects.get(id=selected_tasks[6][0]),
                              duration_7=selected_tasks[6][1],
                              task_id_8=Tasks.objects.get(id=selected_tasks[7][0]),
                              duration_8=selected_tasks[7][1]
                              )
        routine.save()
        
        return redirect(health_goals)