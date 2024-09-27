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
    class Meta:
        model = Comment
        fields = ["task", "body_text"]


class TaskCommentsSerializer(serializers.ModelSerializer):
    comment_author = serializers.ReadOnlyField(source='get_author')

    class Meta:
        model = Comment
        fields = ["task", "comment_author", "body_text"]
