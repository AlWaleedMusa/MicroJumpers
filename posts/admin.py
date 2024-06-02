from .models import Posts, Comments, Reports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ("title", "author")


admin.site.register(Posts, PostAdmin)
admin.site.register(Comments)


@admin.register(Reports)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "post", "comment", "reason", "created_at")
    list_filter = ("reason", "created_at")
