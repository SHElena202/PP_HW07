from django.contrib.auth import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

