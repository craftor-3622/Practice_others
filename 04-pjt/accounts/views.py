from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import InterestForm
from django.contrib.auth import get_user
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Interest


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('stock_finder')
    else:
        form = AuthenticationForm(request)
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('stock_finder')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
def signout(request):
    request.user.delete()
    return redirect('accounts:login')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def profile(request):
    interests = Interest.objects.filter(user=request.user)
    form = InterestForm()
    context = {
        'interests': interests,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)

def find_company(request, company_name):
    context = {
        'company_name': company_name,
    }
    return render(request, 'contentfetch/stock_finder.html', context)

@login_required
def add_interests(request):
    interest_form = InterestForm(request.POST)
    if interest_form.is_valid():
        interest = interest_form.save(commit=False)
        interest.user = request.user
        interest.save()
        return redirect("accounts:profile")
    context = {
        'interest': interest,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def delete_interests(request, interest_pk):
    interest = Interest.objects.get(pk=interest_pk)
    if request.user == interest.user:
        interest.delete()
    return redirect("accounts:profile")