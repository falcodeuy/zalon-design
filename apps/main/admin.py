from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Pack,
    Illustration,
    Customer,
    CustomerReview,
    Order,
    ContactMsg,
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
            '<img src="{}" width="40" height="30" />'.format(obj.image.url)
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
    search_fields = ("name", "subtitle")
    ordering = ("name",)

    class IllustrationInline(admin.TabularInline):
        model = Illustration
        extra = 0
        readonly_fields = ("display_preview",)

        def display_preview(self, obj):
            return format_html('<img src="{}" width="40" height="30" />', obj.image.url)

        display_preview.short_description = "Preview"

    inlines = [IllustrationInline]

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="80" height="60" />'.format(obj.cover.url)
        )

    image_tag.short_description = "cover"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_illustrations(form.instance)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "pack",
    )
    search_fields = (
        "customer__name",
        "customer__email",
        "customer__business",
        "customer__phone",
        "review",
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "email", "phone")
    search_fields = ("name", "business", "email", "phone")
    ordering = ("name", "business", "email", "phone")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "pack",
        "is_reviewed",
        "review_request_sent",
        "created_at",
    )
    search_fields = (
        "customer__name",
        "customer__email",
        "customer__business",
        "customer__phone",
        "pack__name",
    )
    ordering = ("customer", "pack", "created_at")
    readonly_fields = (
        "customer",
        "pack",
        "created_at",
        "is_reviewed",
        "review_request_sent",
        "payment",
    )
    list_filter = ("is_reviewed",)

    def send_email(self, request, queryset):
        for order in queryset:
            print(f"Enviando email a {order.customer.email}...")

    send_email.short_description = "Pedir reseña por email"
    actions = [send_email]


@admin.register(ContactMsg)
class ContactMsgAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    ordering = ("-created_at", "name", "email")
    readonly_fields = ("name", "email", "message", "created_at")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "customer_email",
        "created_at",
        "last_modified",
        "amount",
    )
    search_fields = ("order__customer__email",)
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

    def order_id(self, obj):
        return obj.order.id

    def customer_email(self, obj):
        return obj.order.customer.email
