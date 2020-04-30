from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from taskmanager.models import Project, Task, Journal, Status

from taskmanager.forms import NewTaskForm, NewJournalForm


# View associee a la liste des projets
@login_required
def projects(request):
    user = request.user
    list_projects = Project.objects.filter(members=user)  # On affiche uniquement les projets de l'utilisateur connecte
    return render(request, 'list_projects.html', locals())


# View associée a un projet et a la liste des taches
@login_required
def project(request, id_project):
    user = request.user
    project = Project.objects.get(id=id_project)
    list_tasks = Task.objects.filter(project=project)  # on affiche la la liste des taches du projet
    return render(request, 'project.html', locals())


# La view associee a une tache
@login_required
def task(request, id_task):
    user = request.user
    task = Task.objects.get(id=id_task)
    project = Project.objects.get(id=task.project.id)
    list_journals = Journal.objects.filter(task=task)  # La liste des entrees journal associees a la tache
    return render(request, 'task.html', locals())


# View associee a la creation de tache
@login_required
def newtask(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            form.save() # on sauvegarde

            project = form['project'].value()

            return task(request, form.instance.id) # on affiche la page associee a cette tache

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newtask.html', locals())


# VIew associee a l'update d'une tache
@login_required
def updatetask(request, id_task):
    utask = Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST, instance=utask)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            # On recupere els informations du form
            utask.project = form.cleaned_data['project']
            utask.name = form.cleaned_data['name']
            utask.description = form.cleaned_data['description']
            utask.assignee = form.cleaned_data['assignee']
            utask.due_date = form.cleaned_data['due_date']
            utask.start_date = form.cleaned_data['start_date']
            utask.priority = form.cleaned_data['priority']
            utask.status = form.cleaned_data['status']
            utask.save()  # on modifie l'entree dans la database

            project = form['project'].value()

            return task(request, utask.id)  # On redirige vers la tache

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm(request.POST, instance=utask)
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'updatetask.html', locals())


# View associee a l'entree d'un journal
@login_required
def newjournal(request, id_task):
    jtask = Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewJournalForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()

            return task(request, jtask.id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewJournalForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newjournal.html', locals())
