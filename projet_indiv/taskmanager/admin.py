from django.contrib import admin
from .models import Project, Task, Status, Journal

# Models we can manage from Django administration

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Journal)
