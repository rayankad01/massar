from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    massarID = models.EmailField(unique=True)
    classe = models.CharField(max_length=300, null=True)
    displayed_password = models.BinaryField( null=True)
    def __str__(self):
        return self.username

