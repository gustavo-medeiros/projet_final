from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)

    class Meta:
        ordering = []

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = []

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete = models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.ForeignKey(Status, on_delete = models.CASCADE)

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return self.name


class Journal(models.Model):
    date = models.DateField()
    entry = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.entry







class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
