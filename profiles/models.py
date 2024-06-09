from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User profile model"""

    WORK_EXPERIENCE = [
        (1, "1 year"),
        (2, "2 years"),
        (3, "3 years"),
        (4, "4 years"),
        (5, "5 years"),
        (6, "6 years"),
        (7, "7 years"),
        (8, "8 years"),
        (9, "9 years"),
        (10, "10+ years"),
    ]

    USER_TYPE = [
        ("Technician", "Technician"),
        ("Store owner", "Store owner"),
        ("Client", "Client"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to="profile_pics", null=True, blank=True, default="default_profile.jpg"
    )
    user_type = models.CharField(max_length=100, null=True, blank=True, choices=USER_TYPE)
    location = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    work_experience = models.IntegerField(null=True, blank=True, choices=WORK_EXPERIENCE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
