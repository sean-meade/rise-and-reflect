from django.shortcuts import render
from .forms import CommitmentsForm

def daily_commit(request):
    return render(request, 'daily-commit/daily-commit2.html', {'form': CommitmentsForm})

def submit_commitments(request):
    if request.POST:
        form = CommitmentsForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'home/index.html')
    return render(request, 'daily-commit/daily-commit2.html', {'form': CommitmentsForm})