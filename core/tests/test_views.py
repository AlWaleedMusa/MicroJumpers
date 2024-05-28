from core.views import *
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):
    """Test views."""

    def test_landing_page_view(self):
        """Test landing page view."""
        client = Client()
        response = client.get(reverse("landing_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing_page.html")

    def test_notloggedin_user_home_view(self):
        """Test home view for not logged in user."""
        client = Client()
        response = client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/home/")
        self.assertTemplateNotUsed(response, "core/home.html")

    def test_loggedin_user_home_view(self):
        """Test home view for logged in user."""
        user = User.objects.create_user(username="testuser", password="testpassword")
        client = Client()
        client.login(username="testuser", password="testpassword")
        response = client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
