from django.contrib import admin

from .models import Pack, Illustration


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "show_in_landing")
    list_filter = ("is_active", "show_in_landing")
    search_fields = ("name", "description")
    ordering = ("name", "price")
    fieldsets = (
        (None, {"fields": ("name", "price")}),
        (
            "Contenido",
            {
                "fields": (
                    "subtitle",
                    "description",
                )
            },
        ),
        ("Banderas", {"fields": ("is_active", "show_in_landing")}),
    )

    class IllustrationInline(admin.StackedInline):
        model = Illustration
        extra = 0

    inlines = [IllustrationInline]
