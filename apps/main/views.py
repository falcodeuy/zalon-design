from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Pack, CustomerReview, Order
from .forms.order_form import OrderForm
from .forms.customer_review import CustomerReviewForm


def home(request):
    packs = Pack.objects.filter(is_active=True, show_in_landing=True)
    customer_reviews = CustomerReview.objects.all()[:25]
    context = {"packs": packs, "customer_reviews": customer_reviews}
    return render(request, "main/home.html", context)


def pack_detail(request, id):
    pack = Pack.objects.get(id=id)
    context = {"pack": pack}
    return render(request, "main/pack_detail.html", context)


def order_form(request, pack_id):
    if request.method == "POST":
        form = OrderForm(request.POST, pack_id=pack_id)
        if form.is_valid():
            order = form.save()
            return HttpResponseRedirect(f"/thanks/?order={order.id}")
        else:
            return HttpResponseRedirect("/error/")

    else:
        form = OrderForm(pack_id=pack_id)
    context = {"form": form}
    return render(request, "main/order_form.html", context)


def thanks(request):
    order_id = request.GET.get("order")
    order = Order.objects.get(id=order_id)
    context = {"order": order, "pack": order.pack, "customer": order.customer}
    return render(request, "main/thanks.html", context)


def customer_review(request, pack_id, customer_id):
    if request.method == "POST":
        form = CustomerReviewForm(
            request.POST, pack_id=pack_id, customer_id=customer_id
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/thanks/")
        else:
            return HttpResponseRedirect("/error/")

    else:
        form = CustomerReviewForm(pack_id=pack_id, customer_id=customer_id)
    context = {"form": form}
    return render(request, "main/review.html", context)
