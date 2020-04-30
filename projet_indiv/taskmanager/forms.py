from django.forms import forms, ModelForm

from taskmanager.models import Task


class NewTaskForm(ModelForm):
    class Meta:
        model= Task
        fields = '__all__'
