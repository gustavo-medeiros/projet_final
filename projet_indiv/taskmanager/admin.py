from django.contrib import admin
from .models import Project, Profil, Task, Status, Journal

# Register your models here.

admin.site.register(Project)
admin.site.register(Profil)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Journal)