from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from taskmanager.models import Project, Task, Journal, Status

from taskmanager.forms import NewTaskForm


@login_required
def projects(request):
    user = request.user
    list_projects = Project.objects.filter(members=user)
    return render(request, 'list_projects.html', locals())

@login_required
def project(request, id_project):
    user = request.user
    project = Project.objects.get(id=id_project)
    list_tasks = Task.objects.filter(project=project)
    return render(request, 'project.html', locals())

@login_required
def task(request, id_task):
    user = request.user
    task = Task.objects.get(id=id_task)
    project = Project.objects.get(id=task.project.id)
    list_journals = Journal.objects.filter(task=task)
    return render(request,'task.html', locals())

@login_required
def newtask(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()

            project=form['project'].value()


            return task(request, form.instance.id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm()
        list_projects=Project.objects.all()
        list_users=User.objects.all()
        list_status=Status.objects.all()

    return render(request, 'newtask.html', locals())

@login_required
def updatetask(request,id_task):
    utask=Task.objects.get(id=id_task)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST, instance=utask)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            utask.project=form.cleaned_data['project']
            utask.name = form.cleaned_data['name']
            utask.description = form.cleaned_data['description']
            utask.assignee = form.cleaned_data['assignee']
            utask.due_date = form.cleaned_data['due_date']
            utask.start_date= form.cleaned_data['start_date']
            utask.priority = form.cleaned_data['priority']
            utask.status = form.cleaned_data['status']
            utask.save()


            project=form['project'].value()


            return task(request, utask.id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm(request.POST, instance=utask)
        list_projects=Project.objects.all()
        list_users=User.objects.all()
        list_status=Status.objects.all()

    return render(request, 'updatetask.html', locals())

