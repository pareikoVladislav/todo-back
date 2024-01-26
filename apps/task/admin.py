from django.contrib import admin

from apps.task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'creator', 'created_at')
    list_filter = ('category', 'status', 'creator', 'created_at')
    search_fields = ('title',)
