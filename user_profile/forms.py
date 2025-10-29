from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        else:
            # validate password strength
            try:
                password_validation.validate_password(p1, user=User)
            except forms.ValidationError as e:
                self.add_error('password1', e)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # create profile will be handled by signal
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'birth_date', 'location', 'avatar')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            max_mb = 2
            if avatar.size > max_mb * 1024 * 1024:
                raise forms.ValidationError(f'Avatar file size must be <= {max_mb} MB')
        return avatar


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        cur = self.cleaned_data.get('current_password')
        if not self.user.check_password(cur):
            raise forms.ValidationError('Current password is incorrect.')
        return cur

    def clean(self):
        cleaned = super().clean()
        np1 = cleaned.get('new_password1')
        np2 = cleaned.get('new_password2')
        if np1 and np2 and np1 != np2:
            self.add_error('new_password2', 'New passwords do not match.')
        if np1 and self.user.check_password(np1):
            self.add_error('new_password1', 'New password must be different from the current password.')
        # validate strength
        try:
            password_validation.validate_password(np1, user=self.user)
        except forms.ValidationError as e:
            self.add_error('new_password1', e)
        return cleaned

    def save(self, commit=True):
        new = self.cleaned_data['new_password1']
        self.user.set_password(new)
        if commit:
            self.user.save()
        return self.user
