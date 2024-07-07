from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, SearchForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView
from .models import AsetBaru

class CustomPasswordResetView(PasswordResetView):
    success_url = '/accounts/reset/password/done/'
    email_template_name = 'accounts/custom_password_reset_email.html'


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('dashboard_admin')
            elif user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard_staff')
            elif user is not None and user.is_user:
                login(request, user)
                return redirect('dashboard_user')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'accounts/login.html', {'form': form, 'msg': msg})



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to your desired page after signup
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

# Logout View

def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
# def dashboard_view(request):
#     # Your dashboard logic goes here
#     return render(request, 'dashboard.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def search_view(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = AsetBaru.objects.filter(nama_aset__icontains=query)

            # Iterate through results and attach QR code URL
            for result in results:
                # Assuming qr_code is an ImageField in AsetBaru model
                if result.qr_code:
                    result.qr_code_url = result.qr_code.url  # Adjust according to your model field

    context = {
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request, 'dashboard/search_results.html', context)