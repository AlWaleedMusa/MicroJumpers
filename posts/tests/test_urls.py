from django.test import SimpleTestCase
from django.urls import resolve, reverse
from posts.views import *


class TestUrls(SimpleTestCase):

    def test_add_post_url_resolves(self):
        url = reverse("add_post")
        self.assertEqual(resolve(url).func, add_post)

    def test_tag_view_url_resolves(self):
        url = reverse("tag_view", args=["test"])
        self.assertEqual(resolve(url).func, tag_view)

    def test_post_detail_url_resolves(self):
        url = reverse("post_detail", args=["1"])
        self.assertEqual(resolve(url).func, post_detail)

    def test_delete_post_url_resolves(self):
        url = reverse("delete_post", args=["1"])
        self.assertEqual(resolve(url).func, delete_post)

    def test_edit_post_url_resolves(self):
        url = reverse("edit_post", args=["1"])
        self.assertEqual(resolve(url).func, edit_post)

    def test_add_comment_url_resolves(self):
        url = reverse("add_comment", args=["1"])
        self.assertEqual(resolve(url).func, add_comment)

    def test_edit_comment_url_resolves(self):
        url = reverse("edit_comment", args=["1"])
        self.assertEqual(resolve(url).func, edit_comment)

    def test_delete_comment_url_resolves(self):
        url = reverse("delete_comment", args=["1"])
        self.assertEqual(resolve(url).func, delete_comment)

    def test_like_post_url_resolves(self):
        url = reverse("like_post", args=["1"])
        self.assertEqual(resolve(url).func, like_post)

    def test_like_comment_url_resolves(self):
        url = reverse("like_comment", args=["1"])
        self.assertEqual(resolve(url).func, like_comment)

    def test_bookmark_post_url_resolve(self):
        url = reverse("bookmark_post", args=["1"])
        self.assertEqual(resolve(url).func, bookmark_post)

    def test_mark_solution_url_resolves(self):
        url = reverse("mark_solution", args=["1"])
        self.assertEqual(resolve(url).func, mark_solution)

    def test_report_post_url_resolves(self):
        url = reverse("report_post", args=["1"])
        self.assertEqual(resolve(url).func, report_post)

    def test_report_comment_url_resolves(self):
        url = reverse("report_comment", args=["1"])
        self.assertEqual(resolve(url).func, report_comment)
