import hashlib
import hmac
import os
import urllib.parse
from importlib import import_module

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string


def get_context_data(extra_context=None):
    """This function is used to manually called our custom context preprocessors without having a request"""
    context = {}

    dummy_request = HttpRequest()
    for processor_path in settings.TEMPLATES[0]["OPTIONS"]["context_processors"]:
        module_name, func_name = processor_path.rsplit(".", 1)
        module = import_module(module_name)
        processor = getattr(module, func_name)
        context.update(processor(dummy_request))

    if extra_context:
        context.update(extra_context)

    return context


def send_confirmation_email(order):
    subject = f"Gracias por tu compra - #{order.id}"
    context = get_context_data(
        {
            "order": order,
            "customer": order.customer,
            "pack": order.pack,
        }
    )
    html_content = render_to_string("email/order_confirmation.html", context)
    text_content = "Gracias por tu compra"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.customer.email]
    message = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    message.attach_alternative(html_content, "text/html")

    if order.pack.instructions_file:
        message.attach_file(order.pack.instructions_file.path)

    message.send()


def send_customer_review_request_email(order):
    subject = "¿Te hemos sido de utilidad?"
    context = get_context_data(
        {
            "customer": order.customer,
            "pack": order.pack,
        }
    )
    html_content = render_to_string("email/customer_review_request.html", context)
    text_content = "¿Qué te pareció tu compra?"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.customer.email]
    message = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
    message.attach_alternative(html_content, "text/html")
    message.send()
    order.review_request_sent = True
    order.save()


def send_contact_notification_email(contact_msg):
    subject = f"Nuevo mensaje de contacto en Zalon Design: {contact_msg.name}"
    # Render HTML template
    html_message = render_to_string(
        "email/contact_notification.html",
        {
            "contact_msg": contact_msg,
        },
    )

    email_from = settings.EMAIL_HOST_USER
    recipient_list = settings.CONTACT_EMAILS

    # Pass HTML content as message
    send_mail(subject, None, email_from, recipient_list, html_message=html_message)


def check_mp_signature(request):
    # Obtain the x-signature value from the header
    xSignature = request.headers.get("x-signature")
    xRequestId = request.headers.get("x-request-id")

    # Obtain Query params related to the request URL
    queryParams = urllib.parse.parse_qs(request.GET.urlencode())

    # Extract the "data.id" from the query params
    dataID = queryParams.get("data.id", [""])[0]

    # Separating the x-signature into parts
    parts = xSignature.split(",")

    # Initializing variables to store ts and hash
    ts = None
    hash = None

    # Iterate over the values to obtain ts and v1
    for part in parts:
        # Split each part into key and value
        keyValue = part.split("=", 1)
        if len(keyValue) == 2:
            key = keyValue[0].strip()
            value = keyValue[1].strip()
            if key == "ts":
                ts = value
            elif key == "v1":
                hash = value

    # Obtain the secret key for the user/application from Mercadopago developers site
    secret = os.environ.get("MP_WEBHOOKS_SECRET_KEY")

    # Generate the manifest string
    manifest = f"id:{dataID};request-id:{xRequestId};ts:{ts};"

    # Create an HMAC signature defining the hash type and the key as a byte array
    hmac_obj = hmac.new(
        secret.encode(), msg=manifest.encode(), digestmod=hashlib.sha256
    )

    # Obtain the hash result as a hexadecimal string
    sha = hmac_obj.hexdigest()
    if sha == hash:
        # HMAC verification passed
        return True
    else:
        # HMAC verification failed
        return False
