from django.contrib import admin

from project.tasks.models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "status", ]
    list_select_related = ["owner"]
    list_filter = ('owner', 'status')
    # readonly_fields = ["status"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["task", "author", "body_text", ]
    list_select_related = ["task"]
    list_filter = ('author',)
