from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Pack, CustomerReview
from .forms.pack_purchase import PackPurchaseForm


def home(request):
    packs = Pack.objects.filter(is_active=True, show_in_landing=True)
    customer_reviews = CustomerReview.objects.all()[:25]
    context = {"packs": packs, "customer_reviews": customer_reviews}
    return render(request, "main/home.html", context)


def pack_detail(request, id):
    pack = Pack.objects.get(id=id)
    context = {"pack": pack}
    return render(request, "main/pack_detail.html", context)


def pack_purchase(request, pack_id):
    if request.method == "POST":
        form = PackPurchaseForm(request.POST, pack_id=pack_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/thanks/")
        else:
            return HttpResponseRedirect("/error/")

    else:
        form = PackPurchaseForm(pack_id=pack_id)
    context = {"form": form}
    return render(request, "main/pack_purchase.html", context)
