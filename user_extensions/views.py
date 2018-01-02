from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExtendedUserForm, ExtendedUserProfileForm
from .models import ExtendedUserProfile

def register_user(request):
    '''Register and sign in a new user'''

    if request.method == 'POST':
        form = ExtendedUserForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            profile = ExtendedUserProfile(
                user=user, country='US', timezone='US/Eastern')
            profile.save()

            return redirect('profile')

        else:
            return render(request, 'registration/register.html',
                          {'form': form}, status=400)

    else:

        return render(request, 'registration/register.html',
                      {'form': ExtendedUserForm()},
                      status=200)

@login_required
def update_profile(request):
    '''Update the user profile'''

    try:
        profile = ExtendedUserProfile.objects.get(user=request.user)
    except ExtendedUserProfile.DoesNotExist:
        profile = ExtendedUserProfile(user=request.user)

    if request.method == 'POST':
        form = ExtendedUserProfileForm(request.POST)

        if form.is_valid():

            profile.country = form.cleaned_data.get('country')
            profile.timezone = form.cleaned_data.get('timezone')
            profile.save()

            return render(request, 'registration/profile.html',
                          {'form': ExtendedUserProfileForm(instance=profile)},
                          status=201)

        else:
            return render(request, 'registration/profile.html',
                          {'form': form}, status=400)

    else:
        return render(request, 'registration/profile.html',
                      {'form': ExtendedUserProfileForm(instance=profile)},
                      status=200)
