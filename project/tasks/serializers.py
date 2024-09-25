from rest_framework import serializers

from project.tasks.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ["id", "owner", "title", "description", "status"]

    @staticmethod
    def get_id(obj):
        return obj.id


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
    author = serializers.ReadOnlyField(source='task.owner.username')

    class Meta:
        model = Comment
        fields = ["author", "task_id", "body_text"]

    @staticmethod
    def get_id(obj):
        return obj.id
