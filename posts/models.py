from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
import uuid


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Posts(models.Model):
    """Creating a new post model"""

    id = models.UUIDField(
        max_length=255, default=uuid.uuid4, primary_key=True, unique=True
    )
    title = models.CharField(max_length=255)
    uploaded_image = models.ImageField(
        upload_to="posts_pics",
        null=True,
        blank=True,
        default="default_post.webp",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    solution_comment = models.OneToOneField(
        "Comments",
        on_delete=models.SET_NULL,
        related_name="solution_comment",
        blank=True,
        null=True,
    )
    # solved_by = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name="solved_posts",
    #     blank=True,
    #     null=True,
    # )
    tags = TaggableManager(through=UUIDTaggedItem)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    bookmarks = models.ManyToManyField(
        User, related_name="bookmarked_posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}: {self.title}"

    class Meta:
        """overwriting META"""

        ordering = ["-created_at"]
        verbose_name_plural = "Posts"


class Comments(models.Model):
    """Creating a comment model"""

    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    mark_solution = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} comment on {self.post}"

    class Meta:
        """overwriting META"""

        ordering = ["-created_at"]
        verbose_name_plural = "Comments"

    @classmethod
    def get_top_liked_comments(cls, post, min_likes=3, num_comments=3):
        """
        Retrieve the top liked comments.
        """
        top_liked_comments = cls.objects.filter(post=post).annotate(
            num_likes=Count("likes")
        )
        top_liked_comments = top_liked_comments.exclude(num_likes__lt=min_likes)
        top_liked_comments = top_liked_comments.order_by("-num_likes")[:num_comments]

        return top_liked_comments


class Reports(models.Model):
    """Creating a report model"""

    REPORT_CHOICES = [
        ("SPAM", "Spam"),
        ("INAPPROPRIATE", "Inappropriate"),
        ("OTHER", "Other"),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        Comments, on_delete=models.CASCADE, null=True, blank=True
    )
    reason = models.CharField(max_length=255, choices=REPORT_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report by {self.reporter} on {"Post" if self.post else "Comment"}'

    class Meta:
        """overwriting META"""

        ordering = ["-created_at"]
        verbose_name_plural = "Reports"
