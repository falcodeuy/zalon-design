from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Pack,
    Illustration,
    Customer,
    CustomerReview,
    Order,
    Contact,
    Payment,
)
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
        "image_tag",
    )
    list_filter = ("is_active",)
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
            '<img src="{}" width="133" height="100" />'.format(obj.cover.url)
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
    readonly_fields = ("photo_tag",)

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="48" height="48" />'.format(obj.photo.url)
            )
        else:
            return "Cliente sin foto"

    photo_tag.short_description = "foto"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "pack", "created_at")
    search_fields = ("customer", "pack")
    ordering = ("customer", "pack", "created_at")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    ordering = ("name", "email", "created_at")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "created_at", "last_modified", "amount")
    search_fields = ("order__id",)
    ordering = ("last_modified", "created_at")
    readonly_fields = (
        "order",
        "created_at",
        "last_modified",
        "amount",
        "payment_method",
        "payment_type",
        "payment_status",
        "payment_id",
        "payment_provider",
    )
