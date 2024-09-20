from django.urls import path
from rest_framework.routers import DefaultRouter

from project.tasks.views import TasksListView

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("tasks", TasksListView.as_view(), name="tasks_list"),
    # path("blog/<int:pk>", BlogItemView.as_view(), name="blog_item"),
    # path("blog/blog/<int:pk>", BlogItemDetailView.as_view(), name="blog_detail_comments"),
    # path("blog/add", BlogAddView.as_view(), name="blog_add"),
    # path("blog/comment", CommentAddView.as_view(), name="blog_add_comment"),
    *router.urls,
]
