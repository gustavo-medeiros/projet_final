from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# Definition of a project
class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    class Meta:
        ordering = []

    def __str__(self):
        return self.name


# Definition of a status
class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = []

    def __str__(self):
        return self.name


# Definition of a task
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)

    class Meta:
        ordering = ['-priority']  # Ordered by priority

    def __str__(self):
        return self.name


# Definition of a Journal entry
class Journal(models.Model):
    date = models.DateTimeField(default=datetime.now())  # date/time autofilled (time-zone respected)
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']  # The more recent entry will be on top

    def __str__(self):
        return self.entry


