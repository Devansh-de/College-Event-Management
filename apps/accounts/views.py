from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm # Need to create this form

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            for msg in form.error_messages:
                 messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

# ... login/logout/register views ...

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Exception:
        from .models import Profile
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    # Fetch memberships
    memberships = request.user.club_memberships.all().select_related('club')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'memberships': memberships,
    }
    return render(request, 'accounts/profile.html', context)

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

@login_required
def notification_settings_view(request):
    # Ensure profile exists
    try:
        profile = request.user.profile
    except Exception:
        # Create profile if it doesn't exist (e.g. old users)
        from .models import Profile
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        email_notifications = request.POST.get('email_notifications') == 'on'
        # sms_notifications = request.POST.get('sms_notifications') == 'on'
        
        profile.email_notifications = email_notifications
        profile.save()
        
        messages.success(request, "Notification settings updated!")
        return redirect('profile')
        
    return render(request, 'accounts/notification_settings.html')
