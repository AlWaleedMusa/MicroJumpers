from . import views
from django.urls import path

urlpatterns = [
    path("<str:username>/", views.show_user, name="show_user"),
    path("<str:username>/bookmarks/", views.bookmarks, name="bookmarks"),
    path("<str:username>/posts/", views.user_posts, name="user_posts"),
    path("<str:username>/search/", views.search_profile, name="search-profile"),
]
