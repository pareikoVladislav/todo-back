from django.contrib import admin
from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_superuser',
        'date_joined',
        'last_login'
    ]
    list_filter = ['email', 'is_active', 'date_joined', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
