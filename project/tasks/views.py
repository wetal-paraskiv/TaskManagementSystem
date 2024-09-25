from django.http import JsonResponse
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from project.common.permissions import IsOwnerOrReadOnly
from project.tasks.models import Task, Comment
from project.tasks.serializers import TaskSerializer, TaskListSerializer, MyTaskListSerializer, CommentSerializer


class TaskListView(GenericAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer_class):
        serializer_class.save(owner=self.request.user)

    def get(self, request: Request) -> Response:
        tasks = Task.objects.all()
        return Response(self.get_serializer(tasks, many=True).data)


class MyTaskListView(GenericAPIView):
    serializer_class = MyTaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request: Request) -> Response:
        owner = request.user.id
        if owner:
            tasks = Task.objects.all().filter(owner=request.user.id, status=True)
            response = Response(self.get_serializer(tasks, many=True).data)
        else:
            response = JsonResponse({'Response: ': 'You must LOGIN to access your tasks!'})
        return response


class CompletedTaskListView(GenericAPIView):
    serializer_class = MyTaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

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

    def post(self, request: Request) -> Response:
        #  Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        owner = request.user
        task = Task.objects.create(**validated_data, owner=owner)

        return Response(self.get_id(task))


class TaskDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()


class TaskStatusUpdateView(UpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Task.objects.all()

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.owner == request.user:
            task.status = False
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(f"Task status update completed! id: {task.id}")
            return Response(data="Wrong parameters")
        else:
            return Response("Get your dirty hands OFF! This is not your task!")


class TaskDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Task.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Task deleted successfully!")


class CommentAddView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def post(self, request: Request) -> Response:
        #  Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task_id = validated_data.pop('task_id')
        task = Task.objects.get(task_id)

        comment = Comment.objects.create(**validated_data, task=task)

        return Response(self.get_id(comment))
