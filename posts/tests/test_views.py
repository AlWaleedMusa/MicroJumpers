from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from posts.forms import PostCreation
from posts.models import Posts
from posts.views import *


class TestViews(TestCase):
    """Test views."""

    def setUp(self):
        """setup method."""
        self.user = User.objects.create_user(
            username="testuser", email="test@email.com", password="password"
        )
        self.client = Client()
        self.client.login(username="testuser", password="password")
        self.post = Posts.objects.create(
            id=1,
            title="test post",
            uploaded_image=SimpleUploadedFile(
                "test.jpg", b"file_content", content_type="image/jpeg"
            ),
            author=self.user,
            body="test body",
        )

    def test_add_post_GET(self):
        """Test add post GET."""
        response = self.client.get(reverse("add_post"))
        self.assertEqual(response.status_code, 200)

    def test_add_post_POST(self):
        """Test add post POST"""
        response = self.client.post(
            reverse("add_post"),
            {
                "title": "test post",
                "body": "test body",
                "uploaded_image": SimpleUploadedFile(
                    "test.jpg", b"file_content", content_type="image/jpeg"
                ),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Posts.objects.all().count(), 1)
        self.assertEqual(Posts.objects.all()[0].title, "test post")
        self.assertEqual(Posts.objects.all()[0].body, "test body")
        self.assertEqual(Posts.objects.all()[0].author, self.user)

    def test_tag_view_GET(self):
        """Test tag view GET."""
        response = self.client.get(reverse("tag_view", args=["test"]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_GET(self):
        """Test post detail GET."""
        response = self.client.get(reverse("post_detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_GET(self):
        """Test delete post GET."""
        response = self.client.get(reverse("delete_post", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_edit_post_GET(self):
        """Test edit post GET."""
        response = self.client.get(reverse("edit_post", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_edit_post_POST(self):
        """Test edit post POST."""
        response = self.client.post(
            reverse("edit_post", args=[self.post.id]),
            {
                "title": "test post",
                "body": "test body",
                "uploaded_image": SimpleUploadedFile(
                    "test.jpg", b"file_content", content_type="image/jpeg"
                ),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Posts.objects.all().count(), 1)
        self.assertEqual(Posts.objects.all()[0].title, "test post")
        self.assertEqual(Posts.objects.all()[0].body, "test body")
        self.assertEqual(Posts.objects.all()[0].author, self.user)
