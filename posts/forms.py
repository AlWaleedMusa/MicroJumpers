from .models import Posts, Comments, Reports
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget


class PostCreation(ModelForm):
    """form to create a new post inheriting from model"""

    class Meta:
        model = Posts
        fields = [
            "title",
            "tags",
            "uploaded_image",
            "body",
        ]

        widgets = {
            "body": SummernoteWidget(
                attrs={"summernote": {"width": "100%", "height": "350px"}}
            ),
        }


class CommentCreation(ModelForm):
    """form to create a new comment inheriting from model"""

    class Meta:
        model = Comments
        fields = ["body"]

        widgets = {
            "body": SummernoteWidget(
                attrs={
                    "summernote": {"width": "100%", "height": "280px"},
                }
            )
        }


class ReportForm(ModelForm):
    """form to report a post or comment"""

    class Meta:
        model = Reports
        fields = ["reason", "description"]

        widgets = {
            "description": SummernoteWidget(
                attrs={"summernote": {"width": "100%", "height": "280px"}}
            ),
        }
