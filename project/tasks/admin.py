from django.contrib import admin

from project.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "status", ]
    list_select_related = ["owner"]
    list_filter = ('owner', 'status')
    # readonly_fields = ["status"]
