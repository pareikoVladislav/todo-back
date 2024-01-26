from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from apps.user.views import (
    UserRegistrationGenericView,
)
from apps.jwt_config.views import (
    CustomTokenObtainPairView
)

urlpatterns = [
    path("register/", UserRegistrationGenericView.as_view()),
    path("auth/login/", CustomTokenObtainPairView.as_view()),
    path("auth/refresh-token/", TokenRefreshView.as_view()),
]
