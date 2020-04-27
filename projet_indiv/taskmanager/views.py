from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from taskmanager.models import Project, Task


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



