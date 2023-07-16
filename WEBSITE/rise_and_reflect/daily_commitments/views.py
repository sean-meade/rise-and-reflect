from django.shortcuts import redirect, render
from .forms import CommitmentsForm
from .models import HEALTH_AREAS, UserHealthArea

def daily_commit(request):
    return render(request, 'daily-commit/daily-commit.html', {'form': CommitmentsForm})

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
        form = request.POST
        health_area = UserHealthArea(user=request.user, health_area=request.POST['area'])
        health_area.save()
        return render(request, 'home/index.html')

    return render(request, 'daily-commit/health-goal.html', {'areas': HEALTH_AREAS})
