from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from project.common.permissions import ReadOnly
from project.tasks.models import Task
from project.tasks.serializers import TaskSerializer


class TasksListView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (ReadOnly,)

    def get(self, request: Request) -> Response:
        tasks = Task.objects.all()
        return Response(self.get_serializer(tasks, many=True).data)
