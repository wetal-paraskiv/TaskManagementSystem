from rest_framework import serializers

from project.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ["owner", "title", "description", "status"]
