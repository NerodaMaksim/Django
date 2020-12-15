from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import AuthForm, RegForm
from .models import User
from django import forms
from django.contrib import messages
import datetime
from pathlib import Path
import os
# Create your views here.
LOG_FOLDER = Path('Login/static/logs/')
REGISTRATION_LOG_FILE = LOG_FOLDER / 'registration_log.txt'


def index(request):
    auth_form = AuthForm(request.POST or None)
    if request.method == 'POST' and 'btn-login-form' in request.POST:
        if auth_form.is_valid():
            print(request.POST['username'])
            username = auth_form.data['username']
            password = auth_form.data['psw']
            if check_user_login(username, password):
                # messages.add_message(request, messages.SUCCESS, 'You logged in successfully!!')
                return HttpResponseRedirect('admin_web_page/%s' % username)
            else:
                messages.add_message(request, messages.WARNING, 'Wrong username or password!!')
    return render(request, 'login/login.html', {'form': auth_form})


def check_user_login(username, password):
    all_users = [{'username': user.username,
                  'password': user.password}
                 for user in User.objects.all()]
    print(all_users)
    for current_user in all_users:
        if current_user['username'] == username and str(current_user['password']) == str(password):
            return True
    return False


def check_user_reg(username):
    all_users = [user.username for user in User.objects.all()]
    print(all_users)
    if username in all_users:
        return True
    else:
        return False


def registration(request):
    reg_form = RegForm(request.POST or None)
    reg_log = open(REGISTRATION_LOG_FILE, 'a')
    if request.method == 'POST' and 'btn-reg-form' in request.POST:
        print(request.POST)
        if reg_form.is_valid():
            print(request.POST)
            username = reg_form.data['username']
            password = reg_form.data['psw']
            repeat_password = reg_form.data['psw-repeat']
            print(username + '\n' + password)
            if password != repeat_password:
                messages.add_message(request, messages.WARNING, 'Passwords doesn\'t match')
                reg_log.write(str(datetime.datetime.now()) + '\t' + 'Attempt to registrate user: ' + username
                              + 'Cause: ' + 'Passwords doesn\'t match')
            else:
                if not check_user_reg(username):
                    new_user = User(username=username, password=password, role='user', read_permission=True,
                                    write_permission=False, change_permission=False)
                    new_user.save()
                    reg_log = open(REGISTRATION_LOG_FILE, 'a')
                    reg_log.write(str(datetime.datetime.now()) + '\t' + 'registered user: ' + new_user.username
                                  + '\t' + 'role: ' + new_user.role + '\t'
                                  + 'read_permission: ' + str(new_user.read_permission) + '\t'
                                  + 'write_permission: ' + str(new_user.write_permission) + '\t'
                                  + 'change_permission: ' + str(new_user.change_permission) + '\n')
                    messages.add_message(request, messages.SUCCESS, 'You registered successfully!')
                else:
                    messages.add_message(request, messages.WARNING, 'This username already registered')
                    reg_log.write(str(datetime.datetime.now()) + '\t' + 'Attempt to registrate user: ' + username
                                  + 'Cause: ' + 'This username already registered')
    return render(request, 'registration/registration.html', {'form': reg_form})


def find_user(username):
    all_users = list(User.objects.all())
    for user in all_users:
        if username == user.username:
            return user


def admin_web_page(request, username):
    all_users = list(User.objects.all())
    current_user = find_user(username)
    print(current_user.username + '\t' + current_user.password)
    if current_user.read_permission is False:
        return HttpResponse('You logged in successfully, but you don\'t have permission to read admin page')
    if request.method == 'POST' and 'save-changes-btn' in request.POST:
        print(request.POST)
        for user in all_users:
            if user.username != current_user.username and user.role != 'admin':
                if 'role ' + user.username in request.POST:
                    user.role = request.POST['role ' + user.username]
                if 'read_permission ' + user.username in request.POST:
                    user.read_permission = True
                else:
                    user.read_permission = False
                if 'write_permission ' + user.username in request.POST:
                    user.write_permission = True
                else:
                    user.write_permission = False
                if 'change_permission ' + user.username in request.POST:
                    user.change_permission = True
                else:
                    user.change_permission = False
        for user in all_users:
            user.save()
    return render(request, 'admin/admin.html', {'current_user': current_user,
                                                'all_users': all_users})
