from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from project.common.permissions import IsOwnerOrReadOnly
from project.tasks.models import Task
from project.tasks.serializers import TaskSerializer, TaskListSerializer


class TaskListView(GenericAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request: Request) -> Response:
        tasks = Task.objects.all()
        return Response(self.get_serializer(tasks, many=True).data)


class TaskAddView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # authentication_classes = ()

    def post(self, request: Request) -> Response:
        #  Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        owner = request.user
        task = Task.objects.create(**validated_data, owner=owner)

        return Response(self.serializer_class(task).get_id(task))
