from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from project.common.permissions import IsOwnerOrReadOnly
from project.tasks.models import Task, Comment
from project.tasks.serializers import (
    TaskSerializer,
    TaskListSerializer,
    MyTaskListSerializer,
    CommentSerializer,
    TaskCommentsSerializer)


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

    def get(self, request: Request):
        user = self.request.user
        if user.is_authenticated:
            tasks = user.tasks.all().filter(status=True)
            response = Response(self.get_serializer(tasks, many=True).data)
        else:
            response = Response('You must LOGIN to access your tasks!')
        return response


class CompletedTaskListView(GenericAPIView):
    serializer_class = MyTaskListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request: Request) -> Response:
        user = self.request.user
        if user.is_authenticated:
            tasks = user.tasks.all().filter(status=False)
            response = Response(self.get_serializer(tasks, many=True).data)
        else:
            response = Response('You must LOGIN to access your tasks!')
        return response


class TaskAddView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @staticmethod
    def get_id(obj):
        return obj.id

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

    # linking queryset to get tasks only from logged user
    # def get_queryset(self):
    #     user = self.request.user
    #     return user.tasks.all()


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
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Task deleted successfully!")


class CommentAddView(GenericAPIView):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    permission_classes = (AllowAny,)

    @staticmethod
    def get_id(obj):
        return obj.id

    def post(self, request: Request) -> Response:
        #  Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task = validated_data.pop('task')
        comment = Comment.objects.create(**validated_data, task=task)
        return Response(self.get_id(comment))


class TaskCommentsView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = TaskCommentsSerializer

    def get(self, request, *args, **kwargs) -> Response:
        pk = kwargs['pk']
        comments = Comment.objects.all().filter(task=pk)
        if comments:
            response = Response(self.get_serializer(comments, many=True).data)
        else:
            response = Response('No Task with provided id found!')
        return response
