from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def home_view(request):
    from showcase.models import ShowcaseProject
    latest_projects = ShowcaseProject.objects.all()[:3]
    return render(request, 'home.html', {'latest_projects': latest_projects})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'ইউজারনেম অথবা পাসওয়ার্ড ভুল হয়েছে।')
    return render(request, 'accounts/login.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    from showcase.models import ShowcaseProject
    total = ShowcaseProject.objects.count()
    active = ShowcaseProject.objects.filter(status='active').count()
    completed = ShowcaseProject.objects.filter(status='completed').count()
    recent = ShowcaseProject.objects.all()[:5]
    return render(request, 'dashboard.html', {
        'total': total,
        'active': active,
        'completed': completed,
        'recent': recent,
    })


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if not request.user.check_password(old_password):
            messages.error(request, 'পুরনো পাসওয়ার্ড ভুল।')
        elif new_password != confirm_password:
            messages.error(request, 'নতুন পাসওয়ার্ড মিলছে না।')
        elif len(new_password) < 8:
            messages.error(request, 'পাসওয়ার্ড কমপক্ষে ৮ অক্ষরের হতে হবে।')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'পাসওয়ার্ড সফলভাবে পরিবর্তন হয়েছে।')
            return redirect('profile')
    return render(request, 'accounts/change_password.html')
