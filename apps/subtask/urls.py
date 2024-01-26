from django.urls import path

from apps.subtask.views import (
    SubTasksListGenericView,
    SubTaskDetailGenericView
)


urlpatterns = [
    path("", SubTasksListGenericView.as_view()),
    path("<int:subtask_id>/", SubTaskDetailGenericView.as_view()),
]
