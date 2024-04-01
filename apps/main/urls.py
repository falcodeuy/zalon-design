from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.home, name="home"),
    path("pack/<int:id>/", views.pack_detail, name="pack_detail"),
    path("pack/purchase/<int:id>", views.pack_purchase, name="pack_purchase"),
]
