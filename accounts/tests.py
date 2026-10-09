from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserRole

User = get_user_model()


class Phase1ArchitectureTests(TestCase):
    """
    Automated tests verifying Phase 1 architecture, custom user model, and foundational views.
    """

    def setUp(self):
        self.client = Client()

    def test_custom_user_model_in_use(self):
        """Verify that EduTrack is using accounts.User as the active user model."""
        self.assertEqual(User._meta.label, 'accounts.User')

    def test_all_eight_roles_supported(self):
        """Verify that all 8 institutional roles are present in UserRole choices."""
        role_values = [choice[0] for choice in UserRole.choices]
        expected_roles = [
            'SUPER_ADMIN',
            'COLLEGE_ADMIN',
            'PRINCIPAL',
            'HOD',
            'FACULTY',
            'CLASS_ADVISOR',
            'STUDENT',
            'GUARDIAN'
        ]
        for role in expected_roles:
            self.assertIn(role, role_values)

    def test_role_properties(self):
        """Verify role helper properties on custom user."""
        hod_user = User.objects.create_user(
            username='hod_cs',
            password='TestPassword123!',
            role=UserRole.HOD
        )
        self.assertTrue(hod_user.is_hod)
        self.assertFalse(hod_user.is_student_user)
        self.assertFalse(hod_user.is_guardian)

        student_user = User.objects.create_user(
            username='student_alice',
            password='TestPassword123!',
            role=UserRole.STUDENT
        )
        self.assertTrue(student_user.is_student_user)
        self.assertFalse(student_user.is_hod)

    def test_home_page_loads_successfully(self):
        """Verify that home landing page renders 200 OK with expected branding."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EduTrack')
        self.assertContains(response, 'Smart College Student Management')
        self.assertContains(response, 'progressChart')
