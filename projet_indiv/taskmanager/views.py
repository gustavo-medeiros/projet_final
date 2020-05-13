from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from taskmanager.models import Project, Task, Journal, Status
from taskmanager.forms import NewTaskForm, NewJournalForm
from django.http import HttpResponse, JsonResponse
import csv
import xlwt
from django.core import serializers


# Create your views here.


def projectprogress(project):
    list_tasks = Task.objects.filter(project=project)
    i = 0
    progress = 0
    for task in list_tasks:
        i += 1
        progress += task.progress
    if i==0 :
        i=1
    return (int(progress / i))


# View for the list of projects
@login_required
def projects(request):
    user = request.user
    list_projects = []  # Each cell of list_projects will contains information about a project
    infos = []  # the info cell of a project
    count = 0
    for project in Project.objects.filter(members=user):
        infos.append(
            list(Project.objects.filter(members=user))[count])  # 1st cell of infos contains the members of the project
        infos.append(Task.objects.filter(project=project))  # 2nd cell of infos contains the tasks of the project
        infos.append(Task.objects.filter(project=project).order_by(
            "due_date"))  # 3rd cell of infos contains the tasks of the project ordered by due_date
        list_projects.append(infos)  # add the infos cells in the list of projects
        infos = []
        count += 1
    return render(request,'list_projects.html',locals())




# View for the display of a project and its details
@login_required
def project(request, id_project):
    user = request.user
    project = Project.objects.get(id=id_project)
    list_tasks = Task.objects.filter(project=project)  # List of the tasks of this project
    progress=projectprogress(project)
    return render(request, 'project.html', locals())


# View for the display of a task and its details
@login_required
def task(request, id_task):
    user = request.user
    task = Task.objects.get(id=id_task)
    project = Project.objects.get(id=task.project.id)
    list_journals = Journal.objects.filter(task=task)  # List of the Journal entries of this task
    return render(request, 'task.html', locals())


# View to fill a form to create a task and add it to the database
@login_required
def newtask(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            project = form['project'].value()
            return task(request, form.instance.id)  # if the form is valid, save it in database and display the new task
        else:  # if not, initialize the form and display the form
            form = NewTaskForm()
            list_projects = Project.objects.all()
            list_users = User.objects.all()
            list_status = Status.objects.all()
            return render(request, 'newtask.html', locals())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newtask.html', locals())


# View to update a task
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

            # Get the data from the form
            utask.project = form.cleaned_data['project']
            utask.name = form.cleaned_data['name']
            utask.description = form.cleaned_data['description']
            utask.assignee = form.cleaned_data['assignee']
            utask.due_date = form.cleaned_data['due_date']
            utask.start_date = form.cleaned_data['start_date']
            utask.priority = form.cleaned_data['priority']
            utask.status = form.cleaned_data['status']
            utask.save()  # Update data in database

            project = form['project'].value()

            return task(request, utask.id)  # Display the updated task

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTaskForm(request.POST, instance=utask)
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'updatetask.html', locals())


# View to add a new journal entry
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
            # save
            # redirect to a new URL:
            form.save()
            return task(request, jtask.id)
        else:
            form = NewJournalForm()
            list_projects = Project.objects.all()
            list_users = User.objects.all()
            list_status = Status.objects.all()

        return render(request, 'newjournal.html', locals())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewJournalForm()
        list_projects = Project.objects.all()
        list_users = User.objects.all()
        list_status = Status.objects.all()

    return render(request, 'newjournal.html', locals())


@login_required
def mytasks(request):
    user = request.user
    list_tasks = Task.objects.filter(assignee=user)
    list_projects = Project.objects.filter(members=user)
    chart_data=[]
    for project in list_projects:
        chart_data.append(Task.objects.filter(assignee=user,project=project).count())
    return (render(request, 'mytasks.html', locals()))


@login_required
def donetasks(request):
    user = request.user
    done_status = Status.objects.get(name="Terminée")
    list_tasks = Task.objects.filter(assignee=user, status=done_status)
    return (render(request, 'donetasks.html', locals()))


@login_required
def activity(request, id_project):
    user = request.user
    project = Project.objects.get(id=id_project)
    list_journals = Journal.objects.filter(task__project=project).order_by('-date')
    list_members = Project.objects.get(id=id_project).members.all()
    contributions = []
    for member in list_members:
        contributions.append(nb_contribution(User.objects.get(username=member.username), Project.objects.get(id=id_project)))

    return (render(request, 'activity.html', locals()))

@login_required
def gantt(request,id_project):
    list_members=Project.objects.get(id=id_project).members.all()
    contributions=[]
    for member in list_members:
        contributions.append(nb_contribution(User.objects.get(username=member.username),Project.objects.get(id=id_project)))
    return(render(request,'gantt.html',locals()))

def nb_contribution(user,project):
    n=Journal.objects.filter(task__project=project,author=user).count()
    return(n)


@login_required
def export(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        data_type = request.POST['data-type']
        if file_format == 'CSV':
            response = HttpResponse(content_type='text/csv')
            writer = csv.writer(response)
            if data_type == 'Projects':
                response['Content-Disposition'] = 'attachment; filename="projects.csv"'
                writer.writerow(['Project', 'Members', 'Tasks'])
                for p in Project.objects.all():
                    members = ''
                    for m in p.members.all():
                        members += ', ' + m.username
                    members = members.replace(',', '', 1)

                    tasks = ''
                    for t in p.task_set.all():
                        tasks += ',' + t.name
                    tasks = tasks.replace(',', '', 1)

                    writer.writerow([p.name, members, tasks])
                return response
            if data_type == 'Tasks':
                response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
                writer.writerow(['Name', 'Project', 'Description', 'Assignee', 'Start Date', 'Due Date', 'Priority', 'Status', 'Progress'])
                for t in Task.objects.all():
                    writer.writerow([t.name, t.project, t.description, t.assignee, t.start_date, t.due_date, t.priority, t.status, t.progress])
                return response
            if data_type == 'Journals':
                response['Content-Disposition'] = 'attachment; filename="journals.csv"'
                writer.writerow(['Entry', 'Date', 'Author', 'Task'])
                for j in Journal.objects.all():
                    writer.writerow([j.entry, j.date, j.author, j.task])
                return response
            if data_type == 'Status':
                response['Content-Disposition'] = 'attachment; filename="status.csv"'
                writer.writerow(['Name'])
                for s in Status.objects.all():
                    writer.writerow([s.name])
                return response
        if file_format == 'JSON':
            if data_type == 'Projects':
                projects_list = []
                for p in Project.objects.all():
                    members = ''
                    for m in p.members.all():
                        members += ',' + m.username
                    members = members.replace(',', '', 1)

                    tasks = ''
                    for t in p.task_set.all():
                        tasks += ',' + t.name
                    tasks = tasks.replace(',', '', 1)

                    projects_list.append({"name": p.name, "members": members, "tasks": tasks})
                response = HttpResponse(JsonResponse(projects_list, safe=False), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="projects.json"'
                return response
            if data_type == 'Tasks':
                tasks = Task.objects.all().values('name', 'project__name', 'description', 'assignee__username', 'start_date', 'due_date', 'priority', 'status__name', 'progress')  # or simply .values() to get all fields
                tasks_list = list(tasks)  # important: convert the QuerySet to a list object
                response = HttpResponse(JsonResponse(tasks_list, safe=False), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="tasks.json"'
                return response
            if data_type == 'Journals':
                journals = Journal.objects.all().values('entry', 'date', 'author__username', 'task__name')  # or simply .values() to get all fields
                journals_list = list(journals)  # important: convert the QuerySet to a list object
                response = HttpResponse(JsonResponse(journals_list, safe=False), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="journals.json"'
                return response
            if data_type == 'Status':
                status = Status.objects.all().values('name')  # or simply .values() to get all fields
                status_list = list(status)  # important: convert the QuerySet to a list object
                response = HttpResponse(JsonResponse(status_list, safe=False), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="status.json"'
                return response
        if file_format == 'XLS (Excel)':
            response = HttpResponse(content_type='application/ms-excel')
            if data_type == 'Projects':
                response['Content-Disposition'] = 'attachment; filename="projects.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Projects')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['Project', 'Members', 'Tasks']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                for p in Project.objects.all():
                    members = ''
                    for m in p.members.all():
                        members += ',' + m.username
                    members = members.replace(',', '', 1)

                    tasks = ''
                    for t in p.task_set.all():
                        tasks += ',' + t.name
                    tasks = tasks.replace(',', '', 1)

                    row_num += 1
                    ws.write(row_num, 0, p.name, font_style)
                    ws.write(row_num, 1, members, font_style)
                    ws.write(row_num, 2, tasks, font_style)

                wb.save(response)
                return response
            if data_type == 'Tasks':
                response['Content-Disposition'] = 'attachment; filename="tasks.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Tasks')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['Name', 'Project', 'Description', 'Assignee', 'Start Date', 'Due Date', 'Priority', 'Status', 'Progress']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                for t in Task.objects.all():
                    row_num += 1
                    ws.write(row_num, 0, t.name, font_style)
                    ws.write(row_num, 1, t.project.name, font_style)
                    ws.write(row_num, 2, t.description, font_style)
                    ws.write(row_num, 3, t.assignee.username, font_style)
                    ws.write(row_num, 4, t.start_date.strftime("%Y-%m-%d"), font_style)
                    ws.write(row_num, 5, t.due_date.strftime("%Y-%m-%d"), font_style)
                    ws.write(row_num, 6, t.priority, font_style)
                    ws.write(row_num, 7, t.status.name, font_style)
                    ws.write(row_num, 8, t.progress, font_style)

                wb.save(response)
                return response
            if data_type == 'Journals':
                response['Content-Disposition'] = 'attachment; filename="journals.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Journals')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['Entry', 'Date', 'Author', 'Task']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                for j in Journal.objects.all():
                    row_num += 1
                    ws.write(row_num, 0, j.entry, font_style)
                    if j.date:
                        ws.write(row_num, 1, j.date.strftime("%Y-%m-%d %H:%M"), font_style)
                    ws.write(row_num, 2, j.author.username, font_style)
                    ws.write(row_num, 3, j.task.name, font_style)

                wb.save(response)
                return response
            if data_type == 'Status':
                response['Content-Disposition'] = 'attachment; filename="status.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Status')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                ws.write(row_num, 0, 'Name', font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                for s in Status.objects.all():
                    row_num += 1
                    ws.write(row_num, 0, s.name, font_style)

                wb.save(response)
                return response
        if file_format == 'XML':
            if data_type == 'Projects':
                data = serializers.serialize("xml", Project.objects.all())
                response = HttpResponse(data, content_type='text/xml')
                response['Content-Disposition'] = 'attachment; filename="projects.xml"'
                return response
            if data_type == 'Tasks':
                data = serializers.serialize("xml", Task.objects.all())
                response = HttpResponse(data, content_type='text/xml')
                response['Content-Disposition'] = 'attachment; filename="tasks.xml"'
                return response
            if data_type == 'Journals':
                data = serializers.serialize("xml", Journal.objects.all())
                response = HttpResponse(data, content_type='text/xml')
                response['Content-Disposition'] = 'attachment; filename="journals.xml"'
                return response
            if data_type == 'Status':
                data = serializers.serialize("xml", Status.objects.all())
                response = HttpResponse(data, content_type='text/xml')
                response['Content-Disposition'] = 'attachment; filename="status.xml"'
                return response
    return render(request, 'export.html')