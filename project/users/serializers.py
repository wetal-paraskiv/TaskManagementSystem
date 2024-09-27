from django.contrib.auth.models import User
from rest_framework import serializers

from project.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password",
        )


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')
    # fullname = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "full_name",
            # "fullname",
        )

    def get_fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'
