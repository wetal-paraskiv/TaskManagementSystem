from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from project.users.models import CustomUser
from project.users.serializers import UserSerializer, UserListSerializer, LoginSerializer

from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserList(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer


class UserDetail(RetrieveAPIView):
    queryset = CustomUser.objects.all()
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
        user = CustomUser.objects.create(
            **validated_data,
            is_superuser=False,
            is_staff=False,
        )

        # Set password
        user.set_password(password)
        user.save()

        return Response(self.serializer_class(user).data)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            response = JsonResponse(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
        else:
            response = JsonResponse({'response': 'Unknown user, please register the account!'})
        return response
