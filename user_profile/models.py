from django.db import models
from django.conf import settings


class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(blank=True, null=True)
	location = models.CharField(max_length=150, blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

	def __str__(self):
		return f"Profile of {self.user.username}"
