from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

from .forms import RegistrationForm, UserProfileForm, PasswordChangeForm
from .models import UserProfile

User = get_user_model()


def register_view(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# authenticate and login
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(request, username=user.username, password=raw_password)
			if user:
				login(request, user)
				messages.success(request, 'Registration successful. You are now logged in.')
				return redirect(reverse('user_profile:profile', args=[user.username]))
			return redirect('account_login')
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = RegistrationForm()
	return render(request, 'user_profile/register.html', {'form': form})


@login_required
def edit_profile_view(request):
	profile = getattr(request.user, 'profile', None)
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile updated successfully.')
			return redirect(reverse('user_profile:profile', args=[request.user.username]))
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'user_profile/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Password changed successfully. Please log in again.')
			return redirect(reverse('user_profile:profile', args=[request.user.username]))
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'user_profile/change_password.html', {'form': form})


@login_required
def profile_view(request, username):
	user = get_object_or_404(User, username=username)
	profile = getattr(user, 'profile', None)
	return render(request, 'user_profile/profile.html', {'profile_user': user, 'profile': profile})


@login_required
def delete_account_view(request):
	"""Allow user to delete own account after confirmation."""
	if request.method == 'POST':
		user = request.user
		logout(request)
		username = user.username
		user.delete()
		messages.success(request, f'Account "{username}" deleted successfully.')
		return redirect('user_profile:register')
	return render(request, 'user_profile/delete_account.html')
