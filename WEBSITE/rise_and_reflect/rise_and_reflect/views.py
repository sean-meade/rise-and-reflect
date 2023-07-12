from django.shortcuts import redirect, render
from .forms import *

def register(request):
    if request.method == 'POST':
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = MyCustomSignupForm()
    return render(request, 'allauth/account/signup.html', {'form': form})