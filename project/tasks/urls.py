from django.urls import path
from rest_framework.routers import DefaultRouter

from project.tasks.views import TaskListView, TaskAddView, TaskDetailView, MyTaskListView, CompletedTaskListView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("all", TaskListView.as_view(), name="tasks_list"),
    path("all_my_tasks", MyTaskListView.as_view(), name="all_my_tasks"),
    path("all_my_tasks_completed", CompletedTaskListView.as_view(), name="all_my_tasks_completed"),
    path("add", TaskAddView.as_view(), name="tasks_add"),
    path("<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    *router.urls,
]
