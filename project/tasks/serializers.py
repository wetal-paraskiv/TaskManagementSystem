from rest_framework import serializers

from project.tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ["id", "owner", "title", "description", "status"]


class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = (
            "owner",
            "id",
            "title",
        )


class MyTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='request.user.username')

    class Meta:
        model = Comment
        fields = ["author", "task", "body_text"]


class TaskCommentsSerializer(serializers.ModelSerializer):

    def task(self, obj):
        return obj.task

    class Meta:
        model = Comment
        fields = ["task", "author", "body_text"]
