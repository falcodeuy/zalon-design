from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail


def send_confirmation_email(pack_sale):
    subject = "Gracias por tu compra"
    # Render HTML template
    html_message = render_to_string(
        "email/purchase_confirmation.html",
        {
            "pack_sale": pack_sale,
            "customer": pack_sale.customer,
            "pack": pack_sale.pack,
            "server_name": settings.SERVER_NAME,
        },
    )

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [pack_sale.customer.email]

    # Pass HTML content as message
    send_mail(subject, None, email_from, recipient_list, html_message=html_message)
