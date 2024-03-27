from django.contrib import admin
from django.utils.html import format_html

from .models import Pack, Illustration, CustomerReview


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "is_active",
        "show_in_landing",
        "image_tag",
    )
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
                    "banner",
                )
            },
        ),
        ("Banderas", {"fields": ("is_active", "show_in_landing")}),
    )

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
            '<img src="{}" width="140" height="100" />'.format(obj.banner.url)
        )

    image_tag.short_description = "banner"


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "pack", "image_tag")
    search_fields = ("name", "business", "review")
    ordering = ("name", "business")

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="48" height="48" />'.format(obj.image.url)
        )

    image_tag.short_description = "imagen"
