from . import views
from django.urls import path

urlpatterns = [
    # posts
    path("add/", views.add_post, name="add_post"),
    path("detail/<str:pk>/", views.post_detail, name="post_detail"),
    path("edit/<str:pk>/", views.edit_post, name="edit_post"),
    path("delete/<str:pk>/", views.delete_post, name="delete_post"),
    path("tag_view/<str:slug>/", views.tag_view, name="tag_view"),
    path("like/<str:pk>/", views.like_post, name="like_post"),
    path("bookmark/<str:pk>", views.bookmark_post, name="bookmark_post"),
    # comments
    path("add_comment/<str:pk>/", views.add_comment, name="add_comment"),
    path("edit_comment/<str:pk>/", views.edit_comment, name="edit_comment"),
    path("delete_comment/<str:pk>/", views.delete_comment, name="delete_comment"),
    path("like_comment/<str:pk>/", views.like_comment, name="like_comment"),
]
