from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


from apps.user.views import (
    UserRegistrationGenericView,
)


urlpatterns = [
    path("register/", UserRegistrationGenericView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh-token/", TokenRefreshView.as_view()),
]
