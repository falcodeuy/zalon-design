from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.home, name="home"),
    path(
        "pack/<slug:slug>/",
        views.pack_detail,
        name="pack_detail",
        kwargs={"slug": "slug"},
    ),
]
