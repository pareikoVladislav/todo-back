from django.urls import path

from apps.task.views import (
    TasksListGenericView,
    TaskDetailGenericView
)


urlpatterns = [
    path("", TasksListGenericView.as_view()),
    path("<int:task_id>/", TaskDetailGenericView.as_view()),
]
