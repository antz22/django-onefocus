from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=64, blank=True, null=True)


class Task(models.Model):

    HIGH = '1'
    MEDIUM = '2'
    LOW = '3'

    PRIORITIES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    content = models.TextField()
    completed = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True)
    priority = models.CharField(max_length=6, choices=PRIORITIES, default="3")
    time = models.IntegerField(null=True, blank=True)


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    goal = models.TextField()
    progress = models.IntegerField()
    progressLimit = models.IntegerField()


class Quote(models.Model):
    author = models.TextField()
    content = models.TextField()
