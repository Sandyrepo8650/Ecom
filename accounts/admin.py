from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_login', 'joined_date', 'is_active', 'admin', 'superadmin']
    list_filter = ['admin', 'superadmin']
    list_display_links = ['email', 'first_name']
    filter_horizontal = ()
    fieldsets = (
        (None, {
            'fields': ('email', 'password'),
        }),
        ('Persional Info', {
            'fields': ('first_name', 'last_name', 'phone_number'),
        }),
        ('All Permissions', {
            'fields': ('is_active', 'admin', 'superadmin'),
        }),
    )
    ordering = ()
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)