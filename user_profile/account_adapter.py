from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):
    """Redirect authenticated users to their profile page after login.

    allauth calls get_login_redirect_url without knowledge of the user-specific args,
    so we override it to return the correct URL for the logged-in user.
    """

    def get_login_redirect_url(self, request):
        user = request.user
        if user and user.is_authenticated:
            return reverse('user_profile:profile', args=[user.username])
        return super().get_login_redirect_url(request)
