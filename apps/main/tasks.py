from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.main.models import Order
from apps.main.utils import send_customer_review_request_email


@shared_task
def send_review_reminder_emails():
    seven_days_ago = timezone.now() - timedelta(days=7)
    orders = Order.objects.filter(created_at__lte=seven_days_ago, review_request_sent=False)

    for order in orders:
        send_customer_review_request_email(order)
