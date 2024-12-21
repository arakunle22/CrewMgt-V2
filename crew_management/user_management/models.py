from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    ROLE_CHOICES = [
        ('crew_member', 'Crew Member'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    is_approved = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='crew_member')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"