from django.forms import forms, ModelForm

from taskmanager.models import Task, Journal


class NewTaskForm(ModelForm):
    class Meta:
        model= Task
        fields = '__all__'

class NewJournalForm(ModelForm):
    class Meta:
        model= Journal
        fields = '__all__'