from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    massarID = models.EmailField(unique=True)

    def __str__(self):
        return self.username

