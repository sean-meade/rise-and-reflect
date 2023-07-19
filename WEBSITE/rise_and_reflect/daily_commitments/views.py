from django.shortcuts import redirect, render
from .forms import CommitmentsForm
from .models import HEALTH_AREAS, UserHealthArea
from tasks.models import Tasks
from custom_login.models import UserProfile

def submit_commitments(request):
    if request.POST:
        form = CommitmentsForm(request.POST)
        if form.is_valid():
            commitments = form.save(commit=False)
            commitments.user = request.user
            commitments.save()
        return redirect(health_goals)
    return render(request, 'daily-commit/daily-commit.html', {'form': CommitmentsForm})

def health_goals(request):
    
    if request.POST:
        area = request.POST['area']
        # TODO: check if user has an area already and then overwrite if they do
        # health_area = UserHealthArea(health_area=area)
        # health_area.save()
        user_health_area = UserProfile.objects.filter(user=request.user)
        user_health_area.update(health_area=area)
        area_tasks = Tasks.objects.all().filter(health_area=area)
        
        return render(request, 'tasks/add_tasks.html', {'tasks': area_tasks})

    return render(request, 'daily-commit/health-goal.html', {'areas': HEALTH_AREAS})
