from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def staff(request):
    return render(request, 'dashboard/staff.html')




