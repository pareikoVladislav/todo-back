from django.urls import include, path

urlpatterns = [
    path('users/', include('apps.user.urls')),
    path('categories/', include('apps.category.urls')),
    path('statuses/', include('apps.status.urls')),
    path('tasks/', include('apps.task.urls')),
    path('subtasks/', include('apps.subtask.urls')),
]
