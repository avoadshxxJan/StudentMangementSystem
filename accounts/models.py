from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class UserRole(models.TextChoices):
    """
    Centrally defined institutional roles for EduTrack.
    These 8 roles govern application permissions and department scopes.
    """
    SUPER_ADMIN = 'SUPER_ADMIN', _('Super Administrator')
    COLLEGE_ADMIN = 'COLLEGE_ADMIN', _('College Administrator')
    PRINCIPAL = 'PRINCIPAL', _('Principal')
    HOD = 'HOD', _('Head of Department')
    FACULTY = 'FACULTY', _('Faculty')
    CLASS_ADVISOR = 'CLASS_ADVISOR', _('Class Advisor')
    STUDENT = 'STUDENT', _('Student')
    GUARDIAN = 'GUARDIAN', _('Parent or Guardian')


class User(AbstractUser):
    """
    Custom user model for EduTrack extending Django's AbstractUser.
    Configured as AUTH_USER_MODEL before any database migrations.
    Enforces unique email and institutional role choices.
    """
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_("Unique institutional or primary contact email address.")
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        help_text=_("Institutional access role assigned by an authorized administrator.")
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    @property
    def is_super_admin(self) -> bool:
        return self.role == UserRole.SUPER_ADMIN or self.is_superuser

    @property
    def is_college_admin(self) -> bool:
        return self.role in [UserRole.SUPER_ADMIN, UserRole.COLLEGE_ADMIN] or self.is_superuser

    @property
    def is_principal(self) -> bool:
        return self.role == UserRole.PRINCIPAL

    @property
    def is_hod(self) -> bool:
        return self.role == UserRole.HOD

    @property
    def is_faculty(self) -> bool:
        return self.role in [UserRole.FACULTY, UserRole.CLASS_ADVISOR]

    @property
    def is_class_advisor(self) -> bool:
        return self.role == UserRole.CLASS_ADVISOR

    @property
    def is_student_user(self) -> bool:
        return self.role == UserRole.STUDENT

    @property
    def is_guardian(self) -> bool:
        return self.role == UserRole.GUARDIAN

    def get_role_display_name(self) -> str:
        return dict(UserRole.choices).get(self.role, self.role)

    def __str__(self) -> str:
        name = self.get_full_name() or self.username
        return f"{name} ({self.get_role_display()})"
