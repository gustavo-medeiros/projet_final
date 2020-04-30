from django.forms import forms, ModelForm

from taskmanager.models import Task, Journal


# Un form a partir du model d'une tache
class NewTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'


# Un form a partir du modele d'un journal
class NewJournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = '__all__'
