from . import views
from django.urls import path

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("home/", views.home, name="home"),
    path("search/", views.search, name="search"),
]
