from django.shortcuts import redirect, render
from .forms import CommitmentsForm
from .models import HEALTH_AREAS, UserHealthArea
from tasks.models import Tasks
from custom_login.models import UserProfile

def submit_commitments(request):

    if request.POST:
        # grab data from form
        form = CommitmentsForm(request.POST)
        # If the form submitted by user is valid
        if form.is_valid():
            # Save that info (but don't commit yet)
            commitments = form.save(commit=False)
            # Add the user
            commitments.user = request.user
            # then save
            commitments.save()
        # Take user to the page where they can choose their health area
        return redirect(health_areas)
    # display an empty form on GET request
    return render(request, 'daily-commit/daily-commit.html', {'form': CommitmentsForm})

def health_areas(request):
    # When user presses a button to choose health area
    if request.POST:
        # grab the health area
        area = request.POST['area']
        # Get the user profile of the user
        user_profile = UserProfile.objects.filter(user=request.user)
        # Add health area
        user_profile.update(health_area=area)
        # Grab the tasks related to the health ares
        area_tasks = Tasks.objects.all().filter(health_area=area)
        # send tasks to page for user to choose what to add
        return render(request, 'tasks/add_tasks.html', {'tasks': area_tasks})
    # On GET request send data to create health area buttons
    return render(request, 'daily-commit/health-area.html', {'areas': HEALTH_AREAS})
