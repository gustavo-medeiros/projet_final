from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# Definition d'un projet


class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    class Meta:
        ordering = []

    def __str__(self):
        return self.name


# Definition d'un status
class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = []

    def __str__(self):
        return self.name


# Definition d'une tache
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name


# Definition d'une entree dans le journal
class Journal(models.Model):
    date = models.DateTimeField(default=datetime.now())
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.entry


