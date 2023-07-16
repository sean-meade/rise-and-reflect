from django.shortcuts import render


def daily_commit(request):
    return render(request, 'daily-commit/daily-commit.html')
