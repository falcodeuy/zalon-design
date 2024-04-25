from typing import Any
from django.contrib import admin
from django.utils.html import format_html

from .models import Pack, Illustration, Customer, CustomerReview, PackSale
from .forms.admin import PackAdminForm


@admin.register(Illustration)
class IllustrationAdmin(admin.ModelAdmin):
    list_display = ("pack", "image_tag")
    search_fields = ("pack",)
    ordering = ("pack",)

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="48" height="48" />'.format(obj.image.url)
        )

    image_tag.short_description = "ilustración"


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    form = PackAdminForm

    list_display = (
        "name",
        "price",
        "is_active",
        "show_in_landing",
        "image_tag",
    )
    list_filter = ("is_active", "show_in_landing")
    search_fields = ("name", "description")
    ordering = ("name",)

    class IllustrationInline(admin.TabularInline):
        model = Illustration
        extra = 0
        readonly_fields = ("display_preview",)

        def display_preview(self, obj):
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

        display_preview.short_description = "Preview"

    inlines = [IllustrationInline]

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" />'.format(obj.cover.url)
        )

    image_tag.short_description = "cover"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_illustrations(form.instance)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "pack", "image_tag")
    search_fields = ("customer", "review")

    def image_tag(self, obj):
        if obj.customer.photo:
            return format_html(
                '<img src="{}" width="48" height="48" />'.format(obj.customer.photo.url)
            )
        else:
            return "Cliente sin foto"

    image_tag.short_description = "imagen"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "email", "phone")
    search_fields = ("name", "business", "email", "phone")
    ordering = ("name", "business", "email", "phone")


@admin.register(PackSale)
class PackSaleAdmin(admin.ModelAdmin):
    list_display = ("customer", "pack", "created_at")
    search_fields = ("customer", "pack")
    ordering = ("customer", "pack", "created_at")
