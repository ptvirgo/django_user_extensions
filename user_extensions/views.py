from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import ExtendedUserCreationForm


def register(request):
    '''Register and sign in a new user'''

    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = ExtendedUserCreationForm()

    return render(request, 'registration/register.html',
                  {'form': form},  status=400)
