from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from project.users.serializers import UserSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request: Request) -> Response:
        #  Validate data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Get password from validated data
        password = validated_data.pop("password")

        # Create user
        user = User.objects.create(
            **validated_data,
            is_superuser=True,
            is_staff=True,
        )

        # Set password
        user.set_password(password)
        user.save()

        return Response(self.serializer_class(user).data)
