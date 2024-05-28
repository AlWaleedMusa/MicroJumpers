from .models import Posts, Comments
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ("title", "author")



admin.site.register(Posts, PostAdmin)
admin.site.register(Comments)