from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from accounts.models import UserRole
from config.settings import get_bool_env

User = get_user_model()


class Phase1FoundationTests(TestCase):
    """
    Automated tests verifying Phase 1 foundation requirements:
    - Custom user model & role configuration
    - Email uniqueness & password hashing
    - Home view & template resolution
    - Settings, static files & template directories
    """

    def setUp(self):
        self.client = Client()

    def test_01_custom_user_model_configured(self):
        """1. Verify that accounts.User is the configured authentication model."""
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.User')
        self.assertEqual(User._meta.label, 'accounts.User')

    def test_02_all_eight_roles_present(self):
        """2. Verify that all eight application role choices are defined."""
        role_values = [choice[0] for choice in UserRole.choices]
        expected_roles = [
            'SUPER_ADMIN',
            'COLLEGE_ADMIN',
            'PRINCIPAL',
            'HOD',
            'FACULTY',
            'CLASS_ADVISOR',
            'STUDENT',
            'GUARDIAN',
        ]
        for role in expected_roles:
            self.assertIn(role, role_values)
        self.assertEqual(len(role_values), 8)

    def test_03_email_uniqueness_enforced(self):
        """3. Verify that email uniqueness is enforced by the database."""
        User.objects.create_user(
            username='user_one',
            email='duplicate@edutrack.local',
            password='Password123!'
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='user_two',
                email='duplicate@edutrack.local',
                password='DifferentPassword123!'
            )

    def test_04_user_created_with_valid_password(self):
        """4. Verify that a user can be created with a valid password and authenticated."""
        user = User.objects.create_user(
            username='valid_user',
            email='valid@edutrack.local',
            password='ValidPassword123!',
            role=UserRole.STUDENT
        )
        self.assertEqual(user.username, 'valid_user')
        self.assertEqual(user.role, UserRole.STUDENT)
        self.assertTrue(user.check_password('ValidPassword123!'))

    def test_05_passwords_are_hashed(self):
        """5. Verify that passwords are hashed and never stored in plain text."""
        raw_password = 'PlainTextPasswordToHash!'
        user = User.objects.create_user(
            username='hashed_user',
            email='hashed@edutrack.local',
            password=raw_password
        )
        self.assertNotEqual(user.password, raw_password)
        self.assertTrue(user.password.startswith('pbkdf2_') or user.password.startswith('argon2'))

    def test_06_home_page_returns_200(self):
        """6. Verify that the home page returns HTTP 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_07_home_page_uses_expected_template(self):
        """7. Verify that the home page renders the pages/home.html template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'includes/navbar.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_08_admin_url_resolves(self):
        """8. Verify that the Django Admin URL resolves properly."""
        match = resolve('/admin/')
        self.assertEqual(match.app_name, 'admin')

    def test_09_settings_environment_configuration(self):
        """9. Verify settings configuration loads expected development variables."""
        self.assertEqual(settings.TIME_ZONE, 'Asia/Kolkata')
        self.assertTrue(settings.USE_TZ)
        self.assertIn(settings.LANGUAGE_CODE, ['en-in', 'en-us'])
        # Verify that get_bool_env parses development DEBUG setting as True
        self.assertTrue(get_bool_env('DJANGO_DEBUG', True))

    def test_10_static_and_template_settings_configured(self):
        """10. Verify that static file and template settings are correctly configured."""
        self.assertTrue(len(settings.TEMPLATES[0]['DIRS']) > 0)
        self.assertTrue(settings.TEMPLATES[0]['DIRS'][0].is_dir())
        self.assertTrue(len(settings.STATICFILES_DIRS) > 0)
        self.assertTrue(settings.STATICFILES_DIRS[0].is_dir())
        self.assertEqual(settings.STATIC_URL, '/static/')
        self.assertEqual(settings.MEDIA_URL, '/media/')
