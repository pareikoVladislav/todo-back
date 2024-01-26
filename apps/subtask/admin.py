from django.contrib import admin

from apps.subtask.models import SubTask


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    def change_subtasks_register(self, request, queryset):
        for obj in queryset:
            obj.title = obj.title.upper()
            obj.save()

    change_subtasks_register.short_description = 'Up register'

    actions = [
        'change_subtasks_register',
    ]

    list_display = ('title', 'category', 'task', 'status', 'creator', 'created_at')
    list_filter = ('task', 'category', 'status', 'creator', 'created_at')
    search_fields = ('title',)
