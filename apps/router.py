from django.urls import include, path

urlpatterns = [
    path('user/', include('apps.user.urls')),
    path('categories/', include('apps.category.urls')),
    path('statuses/', include('apps.status.urls')),
    path('tasks/', include('apps.task.urls')),
]
