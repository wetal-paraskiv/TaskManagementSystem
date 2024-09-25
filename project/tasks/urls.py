from django.urls import path
from rest_framework.routers import DefaultRouter

from project.tasks.views import (
    TaskListView,
    TaskAddView,
    TaskDetailView,
    MyTaskListView,
    CompletedTaskListView,
    TaskStatusUpdateView,
    TaskDeleteView,
    CommentAddView, )

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("all", TaskListView.as_view(), name="tasks_list"),
    path("all_my_tasks_active", MyTaskListView.as_view(), name="all_my_tasks_active"),
    path("all_my_tasks_completed", CompletedTaskListView.as_view(), name="all_my_tasks_completed"),
    path("<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("add", TaskAddView.as_view(), name="tasks_add"),
    path("update_status/<int:pk>", TaskStatusUpdateView.as_view(), name="task_status_update"),
    path("delete/<int:pk>", TaskDeleteView.as_view(), name="delete_task"),
    path("comment", CommentAddView.as_view(), name="add_comment"),
    *router.urls,
]
