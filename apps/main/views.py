import json
import requests
import os
import mercadopago


from bs4 import BeautifulSoup
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect

from .forms.contact_form import ContactForm
from .models import Pack, CustomerReview, Order, Payment, ContactMsg
from .forms.order_form import OrderForm
from .forms.customer_review_form import CustomerReviewForm
from .utils import check_mp_signature, send_confirmation_email


MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN")
SERVER_NAME = os.environ.get("SERVER_NAME")
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)


def home(request):
    packs = Pack.objects.filter(
        is_active=True,
    )
    customer_reviews = CustomerReview.objects.all()[:25]
    orders_count = Order.objects.count()

    # TODO move this to a service and call it using AJAX to avoid relanting the initial page load
    def get_instagram_followers():
        try:
            url = f"https://www.instagram.com/zalon.app"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            data = soup.find_all("meta", attrs={"property": "og:description"})
            text = data[0].get("content").split()
            followers = text[0]
            return followers.replace(",", ".")
        except Exception as e:
            print(e)
            return "6413"

    context = {
        "packs": packs,
        "customer_reviews": customer_reviews,
        "sold_packs": orders_count
        + 101,  # 101 is a random number to show some activity for marketing purposes
        "instagram_followers": get_instagram_followers(),
    }
    return render(request, "main/home.html", context)


def pack_detail(request, slug):
    try:
        if slug.isnumeric():
            pack = Pack.objects.get(id=slug)
        else:
            pack = Pack.objects.get(custom_url=slug)
        context = {"pack": pack}

        return render(request, "main/pack_detail.html", context)
    except Pack.DoesNotExist:
        return HttpResponseRedirect("/error/")


def order_form(request, pack_id):
    pack = Pack.objects.get(id=pack_id)

    if request.method == "POST":
        form = OrderForm(request.POST, pack_id=pack_id)
        if form.is_valid() and pack.price > 0:
            order = form.save()
            preference_data = {
                "back_urls": {
                    "success": f"https://{SERVER_NAME}/thanks/?order={order.id}",
                    "failure": f"https://{SERVER_NAME}/error/?order={order.id}",
                    "pending": f"https://{SERVER_NAME}/thanks/?order={order.id}",
                },
                "auto_return": "approved",  # if the payment is successful this redirect automatically to success url.
                "metadata": {"zalon_order_id": order.id},
                "items": [
                    {
                        "title": pack.name,
                        "quantity": 1,
                        "unit_price": float(pack.price),
                    }
                ],
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            return HttpResponseRedirect(preference["init_point"])

        elif form.is_valid() and pack.price == 0:
            order = form.save()
            send_confirmation_email(order)
            return HttpResponseRedirect(f"/thanks/?order={order.id}")
        else:
            return HttpResponseRedirect("/error/")

    else:
        form = OrderForm(pack_id=pack_id)
    context = {"form": form, "pack": pack}
    return render(request, "main/order_form.html", context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            return HttpResponseRedirect(
                f"/contact-confirmation/?contact_msg={contact_msg.id}"
            )
        else:
            return HttpResponseRedirect("/error/")
    else:
        form = ContactForm()
    context = {"form": form}
    return render(request, "main/contact.html", context)


def contact_confirmation(request):
    contact_msg = request.GET.get("contact_msg")
    contact_msg = ContactMsg.objects.filter(id=contact_msg).first()
    if not contact_msg:
        return HttpResponseRedirect("/error/")
    context = {"contact_msg": contact_msg}
    return render(request, "main/contact_confirmation.html", context)


def review_confirmation(request):
    return render(request, "main/review_confirmation.html")


def thanks(request):
    order_id = request.GET.get("order")
    order = Order.objects.get(id=order_id)
    context = {"order": order, "pack": order.pack, "customer": order.customer}
    return render(request, "main/thanks.html", context)


def error(request):
    return render(request, "main/error.html")


def customer_review(request):
    pack_id = request.GET.get("pack_id")
    if request.method == "POST":
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/review-confirmation/")
    else:
        form = CustomerReviewForm(initial={"pack": pack_id})
    context = {"form": form, "pack_id": pack_id}
    return render(request, "main/customer_review.html", context)


@login_required
def serve_protected_file(request, file_path):
    """
    View to serve protected files as we don't want to expose the media/instructinos folder to the public.
    """
    document = os.path.join(settings.MEDIA_ROOT, "instructions", file_path)
    if os.path.exists(document):
        return FileResponse(
            open(document, "rb"), content_type="application/force-download"
        )
    else:
        raise Http404("File does not exist")


@csrf_exempt
def mp_notification(request):
    if request.method == "POST":
        # Obtain the x-signature value from the header
        signature_valid = check_mp_signature(request)
        if signature_valid:
            # Extract the data from the request
            body = request.body.decode("utf-8")
            body_dict = json.loads(body)
            payment_id = body_dict["data"]["id"]
            payment_id = body_dict["data"]["id"]
            url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
            headers = {"Authorization": f"Bearer {MP_ACCESS_TOKEN}"}
            response = requests.get(url, headers=headers)

            print(json.dumps(response.json(), indent=4))
            payment_response = response.json()

            ## check if payment already exist, in that case update it
            payment = Payment.objects.filter(payment_id=payment_response["id"]).first()

            if payment:

                payment.payment_status = payment_response["status"]
                payment.last_modified = payment_response["date_last_updated"]
                payment.save()

            else:

                Payment.objects.create(
                    order=Order.objects.get(
                        id=payment_response["metadata"]["zalon_order_id"]
                    ),
                    created_at=payment_response["date_created"],
                    last_modified=payment_response["date_last_updated"],
                    amount=payment_response["transaction_amount"],
                    payment_method=payment_response["payment_method_id"],
                    payment_type=payment_response["payment_type_id"],
                    payment_status=payment_response["status"],
                    payment_id=payment_response["id"],
                    payment_provider="mercadopago",
                )

            return HttpResponse(status=200)
        else:
            return HttpResponse("Invalid signature", status=400)
    else:
        return HttpResponse(status=405)  # Method Not Allowed
