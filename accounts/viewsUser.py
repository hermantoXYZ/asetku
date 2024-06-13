
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def is_user(user):
    return user.is_authenticated and user.is_user

@user_passes_test(is_user)
def user(request):
    return render(request, 'dashboard/user.html')
