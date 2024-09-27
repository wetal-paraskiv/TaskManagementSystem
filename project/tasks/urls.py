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
    CommentAddView,
    TaskCommentsView,
    UpdateTaskOwnerView,
    SearchTaskByTitleView, )

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("all", TaskListView.as_view(), name="tasks_list"),
    path("all_my_tasks_active", MyTaskListView.as_view(), name="all_my_tasks_active"),
    path("all_my_tasks_completed", CompletedTaskListView.as_view(), name="all_my_tasks_completed"),
    path("<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("add", TaskAddView.as_view(), name="tasks_add"),
    path("update_status/<int:pk>", TaskStatusUpdateView.as_view(), name="task_status_update"),
    path("delete/<int:pk>", TaskDeleteView.as_view(), name="delete_task"),
    path("update_task_owner/<int:pk>/<int:user_id>", UpdateTaskOwnerView.as_view(), name="update_task_owner"),
    # path("search_task_by_title/<str:search>", SearchTaskByTitleView.as_view(), name="search_task_by_title"),
    path("comment", CommentAddView.as_view(), name="add_comment"),
    path("comments/<int:pk>", TaskCommentsView.as_view(), name="task_comments"),
    *router.urls,
]
