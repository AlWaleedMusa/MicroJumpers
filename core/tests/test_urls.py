from core.views import *
from django.test import SimpleTestCase
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):
    """Test urls."""

    def test_home_url_resolves(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, home)

    def test_landing_page_url_resolves(self):
        url = reverse("landing_page")
        self.assertEqual(resolve(url).func, landing_page)

    def test_search_url_resolves(self):
        url = reverse("search")
        self.assertEqual(resolve(url).func, search)
