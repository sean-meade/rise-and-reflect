from django.shortcuts import  render

from custom_login.models import UserProfile
from .models import Tasks, PersonalTasks

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

        # Get the health area for the user
        user_profile_obj = UserProfile.objects.get(user=request.user)
        # Add the custom tasks to the database based on the inputs from the user
        for task_name, duration in custom_tasks:

            # Create the task
            this_task = Tasks(health_area=user_profile_obj.health_area, task=task_name, task_type="Evening", custom=True)
            this_task.save()
           
        # get duration and task_id of the users tasks
        all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list('duration', 'task_id')
        # turn it to a list of lists
        all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

        # for every task of the users
        for task in range(len(all_user_tasks_list)):
            # Get the task with the id
            filtered_task = Tasks.objects.get(id = all_user_tasks_list[task][1])
            # Then add type and task to list
            all_user_tasks_list[task].append(filtered_task.task_type)
            all_user_tasks_list[task].append(filtered_task.task)
            all_user_tasks_list[task].append(filtered_task.custom)

        # return all the users tasks
        return render(request, 'tasks/view_tasks.html', {'tasks': all_user_tasks_list})
    

    # Same as above to display tasks for a GET request instead of post
    all_user_tasks_tuple = PersonalTasks.objects.filter(user=request.user).values_list('duration', 'task_id')
    all_user_tasks_list = [list(j) for j in all_user_tasks_tuple]

    for task in range(len(all_user_tasks_list)):
        filtered_task = Tasks.objects.get(id = all_user_tasks_list[task][1])
        all_user_tasks_list[task].append(filtered_task.task_type)
        all_user_tasks_list[task].append(filtered_task.task)
        all_user_tasks_list[task].append(filtered_task.custom)

        
    return render(request, 'tasks/view_tasks.html', {'tasks': all_user_tasks_list, })