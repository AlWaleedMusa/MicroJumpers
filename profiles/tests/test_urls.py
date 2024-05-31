from django.test import SimpleTestCase
from django.urls import resolve, reverse
from profiles.views import *

class TestUrls(SimpleTestCase):
    """Test urls for profiles app"""

    def test_show_user_url(self):
        url = reverse("show_user", args=["testuser"])
        self.assertEqual(resolve(url).func, show_user)

    def test_bookmarks_url(self):
        url = reverse("bookmarks", args=["testuser"])
        self.assertEqual(resolve(url).func, bookmarks)

    def test_user_posts_url(self):
        url = reverse("user_posts", args=["testuser"])
        self.assertEqual(resolve(url).func, user_posts)

    def test_search_profile_url(self):
        url = reverse("search-profile", args=["testuser"])
        self.assertEqual(resolve(url).func, search_profile)
