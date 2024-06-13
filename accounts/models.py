# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_staff = models.BooleanField('Is staff', default=False)
    is_user = models.BooleanField('Is user', default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.username