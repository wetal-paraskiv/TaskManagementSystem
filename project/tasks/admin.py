from django.contrib import admin

from project.tasks.models import Task

admin.site.register(Task)
