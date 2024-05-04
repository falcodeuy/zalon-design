from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.home, name="home"),
    path("pack/<int:id>/", views.pack_detail, name="pack_detail"),
    path("pack/order_form/<int:pack_id>", views.order_form, name="order_form"),
    path(
        "customer_review/<int:pack_id>/<int:customer_id>/",
        views.customer_review,
        name="customer_review",
    ),
    path("mp-notification", views.mp_notification, name="example_view"),
    path("thanks/", views.thanks, name="thanks"),
    path("error/", views.error, name="error"),
    path("contact/", views.contact, name="contact"),
]
