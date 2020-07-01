import logging

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import LoginForm, SignUpFormUser

logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # Session
                    db = User.objects.filter(id=user.pk)
                    if len(db) > 0:
                        if db[0].is_superuser:
                            status = '1'
                        else:
                            status = '0'
                        request.session['id'] = db[0].id
                        request.session['username'] = db[0].username
                        request.session['first_name'] = db[0].first_name
                        request.session['status'] = status
                        request.session['email'] = db[0].email

                    return redirect('home:index')
            else:
                messages.error(request, 'username or password incorrect')
                return redirect('login_view')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpFormUser(request.POST)
        print(form.errors)
        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                user = form.save()
                user.refresh_from_db()
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.is_superuser = False
                user.is_staff = True
                user.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')

                user = authenticate(username=username, password=password)

                login(request, user)

                # Session
                db = User.objects.filter(id=user.pk)
                if len(db) > 0:
                    if db[0].is_superuser:
                        status = '1'
                    else:
                        status = '0'
                    request.session['id'] = db[0].id
                    request.session['username'] = db[0].username
                    request.session['first_name'] = db[0].first_name
                    request.session['status'] = status
                    request.session['email'] = db[0].email

                return redirect('home:index')

    form = SignUpFormUser()
    return render(request, 'signup.html', {'form': form})

