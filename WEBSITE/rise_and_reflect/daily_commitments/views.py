from django.shortcuts import render
from .forms import CommitmentsForm

def daily_commit(request):
    return render(request, 'daily-commit/daily-commit.html', {'form': CommitmentsForm})

def submit_commitments(request):
    if request.POST:
        form = CommitmentsForm(request.POST)
        if form.is_valid():
            commitments = form.save(commit=False)
            commitments.user = request.user
            commitments.save()
        return render(request, 'home/index.html')
    return render(request, 'daily-commit/daily-commit.html', {'form': CommitmentsForm})