from django.urls import path
from rest_framework.routers import DefaultRouter

from project.tasks.views import TaskListView, TaskAddView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("all", TaskListView.as_view(), name="tasks_list"),
    path("add", TaskAddView.as_view(), name="tasks_add"),
    *router.urls,
]
