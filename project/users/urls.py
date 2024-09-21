from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from project.users.views import RegisterUserView, UserList, UserDetail

urlpatterns = [
    path('all', UserList.as_view()),
    path('<int:pk>', UserDetail.as_view()),
    path('register', RegisterUserView.as_view(), name='token_register'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
