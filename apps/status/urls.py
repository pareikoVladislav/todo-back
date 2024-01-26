from django.urls import path

from apps.status.views import (
    StatusListGenericView,
    RetrieveStatusGenericView
)


urlpatterns = [
    path("", StatusListGenericView.as_view()),
    path("<int:status_id>/", RetrieveStatusGenericView.as_view()),
]
