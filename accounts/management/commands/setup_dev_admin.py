from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserRole

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates an initial administrator account for local development verification.'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@edutrack.local'
        password = 'Admin@12345EduTrack'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': UserRole.SUPER_ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'System',
                'last_name': 'Administrator',
            }
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created development administrator: {username} (Password: {password})'))
        else:
            self.stdout.write(self.style.WARNING(f'Administrator user "{username}" already exists.'))
