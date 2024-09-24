from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from urllib3 import request

from project.common.permissions import IsOwnerOrReadOnly
from project.tasks.models import Task
from project.tasks.serializers import TaskSerializer, TaskListSerializer, MyTaskListSerializer


class TaskListView(GenericAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer_class):
        serializer_class.save(owner=self.request.user)

    def get(self, request: Request) -> Response:
        tasks = Task.objects.all()
        return Response(self.get_serializer(tasks, many=True).data)


class MyTaskListView(GenericAPIView):
    serializer_class = MyTaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get(self, request: Request) -> Response:
        owner = request.user.id
        if owner:
            tasks = Task.objects.all().filter(owner=request.user.id)
            response = Response(self.get_serializer(tasks, many=True).data)
        else:
            response = JsonResponse({'Response: ': 'You must LOGIN to access your tasks!'})
        return response


class CompletedTaskListView(GenericAPIView):
    serializer_class = MyTaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get(self, request: Request) -> Response:
        owner = request.user.id
        if owner:
            tasks = Task.objects.all().filter(owner=request.user.id, status=False)
            response = Response(self.get_serializer(tasks, many=True).data)
        else:
            response = JsonResponse({'Response: ': 'You must LOGIN to access your tasks!'})
        return response


class TaskAddView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    # authentication_classes = ()

    def post(self, request: Request) -> Response:
        #  Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        owner = request.user
        task = Task.objects.create(**validated_data, owner=owner)

        return Response(self.serializer_class(task).get_id(task))


class TaskDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()
