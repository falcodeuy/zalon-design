from django.shortcuts import render

from .models import Pack


def home(request):
    packs = Pack.objects.filter(is_active=True, show_in_landing=True)
    context = {"packs": packs}

    return render(request, "main/home.html", context)


def pack_detail(request, slug):
    pack = Pack.objects.get(slug=slug)
    context = {"pack": pack}

    return render(request, "main/pack_detail.html", context)
