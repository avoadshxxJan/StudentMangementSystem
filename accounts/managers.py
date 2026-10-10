from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager for EduTrack.
    Enforces unique email address and sets standard user defaults.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set.'))
        if not email:
            raise ValueError(_('The Email field must be set.'))

        email = self.normalize_email(email)
        # Default role is STUDENT if not specified
        if 'role' not in extra_fields or not extra_fields['role']:
            from accounts.models import UserRole
            extra_fields['role'] = UserRole.STUDENT

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        from accounts.models import UserRole

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.SUPER_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)
