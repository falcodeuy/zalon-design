from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'This file is for scripts or fast test inside the project environment'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        to_email = 'cr.silper@gmail.com'
        from_email = 'noreply@zalon.design'
        subject = 'Test Email from Django using Amazon SES'
        message = 'This is a test email sent from a Django management command using Amazon SES.'

        try:
            send_mail(subject, message, from_email, [to_email])
            self.stdout.write(self.style.SUCCESS(f'Successfully sent test email to {to_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email to {to_email}: {e}'))
