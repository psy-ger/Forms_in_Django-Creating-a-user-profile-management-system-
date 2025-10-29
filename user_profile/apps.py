from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'
    def ready(self):
        # import signals to ensure profile is created on user creation
        try:
            import user_profile.signals  # noqa: F401
        except Exception:
            pass
