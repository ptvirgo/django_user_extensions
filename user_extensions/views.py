from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import ExtendedUserForm, ExtendedUserProfileForm

def register_user(request):
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

        user_form = ExtendedUserForm()
        profile_form = ExtendedUserProfileForm()

    return render(request, 'registration/register.html',
                  {'user_form': user_form, 'profile_form': profile_form},
                  status=200)
