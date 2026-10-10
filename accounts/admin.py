from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Django Admin registration for the EduTrack custom User model.
    Allows administrators to inspect and assign institutional roles securely.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Institutional Role & Audit'), {
            'fields': ('role',),
            'description': _('Application-level role governing future department and module authorization.')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Institutional Role'), {
            'fields': ('email', 'role',),
        }),
    )
