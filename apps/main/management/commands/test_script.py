from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from apps.main.utils import send_customer_review_request_email
from apps.main.models import Order


class Command(BaseCommand):
    help = "This file is for scripts or fast test inside the project environment"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        order = Order.objects.first()
        send_customer_review_request_email(order)
        self.stdout.write(self.style.SUCCESS("Email sent successfully"))
