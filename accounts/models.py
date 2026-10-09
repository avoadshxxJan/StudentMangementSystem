from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Administrator'
    COLLEGE_ADMIN = 'COLLEGE_ADMIN', 'College Administrator'
    PRINCIPAL = 'PRINCIPAL', 'Principal'
    HOD = 'HOD', 'Head of Department'
    FACULTY = 'FACULTY', 'Faculty Member'
    CLASS_ADVISOR = 'CLASS_ADVISOR', 'Class Advisor'
    STUDENT = 'STUDENT', 'Student'
    GUARDIAN = 'GUARDIAN', 'Parent or Guardian'


class User(AbstractUser):
    """
    Custom user model for EduTrack.
    Uses Django's authentication foundation while supporting 8 institution roles.
    """
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        help_text="Primary institutional role assigned by an administrator."
    )
    phone = models.CharField(max_length=20, blank=True, help_text="Contact telephone number.")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    @property
    def is_super_admin(self):
        return self.role == UserRole.SUPER_ADMIN or self.is_superuser

    @property
    def is_college_admin(self):
        return self.role in [UserRole.SUPER_ADMIN, UserRole.COLLEGE_ADMIN] or self.is_superuser

    @property
    def is_principal(self):
        return self.role == UserRole.PRINCIPAL

    @property
    def is_hod(self):
        return self.role == UserRole.HOD

    @property
    def is_faculty(self):
        return self.role in [UserRole.FACULTY, UserRole.CLASS_ADVISOR]

    @property
    def is_class_advisor(self):
        return self.role == UserRole.CLASS_ADVISOR

    @property
    def is_student_user(self):
        return self.role == UserRole.STUDENT

    @property
    def is_guardian(self):
        return self.role == UserRole.GUARDIAN

    def get_role_display_name(self):
        return dict(UserRole.choices).get(self.role, self.role)

    def __str__(self):
        name = self.get_full_name() or self.username
        return f"{name} ({self.get_role_display()})"
