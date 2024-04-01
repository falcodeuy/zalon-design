from django.shortcuts import render

from .models import Pack, CustomerReview


def home(request):
    packs = Pack.objects.filter(is_active=True, show_in_landing=True)
    customer_reviews = CustomerReview.objects.all()[:25]
    context = {"packs": packs, "customer_reviews": customer_reviews}
    return render(request, "main/home.html", context)


def pack_detail(request, id):
    pack = Pack.objects.get(id=id)
    context = {"pack": pack}
    return render(request, "main/pack_detail.html", context)


def pack_purchase(request, id):
    pack = Pack.objects.get(id=id)
    context = {"pack": pack}
    return render(request, "main/pack_purchase_form.html", context)
