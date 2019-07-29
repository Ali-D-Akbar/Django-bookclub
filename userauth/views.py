from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from userauth.forms import UserCreateForm, UserProfileForm, UserLoginForm


def index(request):
    error_message = ''
    try:
        request.session['username']
        return redirect('books:index')
    except KeyError:
        user_form = UserLoginForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                # Redirect to index page.
                return redirect('books:index')
            else:
                error_message = "username/password MISMATCHED!"
    return render(request, 'userauth/index.html', {'user_form': user_form, 'error_message': error_message})


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        # form brings back a plain text string, not an encrypted password
        pw = user.password
        # thus we need to use set password to encrypt the password string
        user.set_password(pw)
        user.save()
        request.session['username'] = user.username
        login(request, user)
        return redirect('books:index')
    return render(request, 'userauth/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def logout_user(request):
    del request.session['username']
    logout(request)
    return redirect('userauth:index')
