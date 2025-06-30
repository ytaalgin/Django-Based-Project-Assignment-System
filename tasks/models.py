from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    username = None  # username alanını kaldırıyoruz
    email = models.EmailField(unique=True)  # email alanını kullanıcı adı olarak kullanıyoruz

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()  # CustomUserManager'i kullanıyoruz

    def __str__(self):
        return self.email


class Unavailability(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Change to CustomUser
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.start_date} to {self.end_date} ({self.reason})"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
