from django.contrib import admin
from .models import (
    Collection,
    ContactSubmission,
    GoogleReview,
    Order,
    OrderItem,
    Product,
    SupportRequest,
    WarrantyClaim,
)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "collection", "price", "in_stock", "updated_at")
    list_filter = ("collection", "in_stock")
    search_fields = ("name", "slug", "collection__name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone", "comment")
    readonly_fields = ("created_at", "updated_at")


@admin.register(WarrantyClaim)
class WarrantyClaimAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "product_name",
        "status",
        "purchase_date",
        "created_at",
    )
    list_filter = ("status", "purchase_date", "created_at")
    search_fields = ("customer_name", "email", "phone", "product_name", "issue")
    readonly_fields = ("created_at", "updated_at")


@admin.register(GoogleReview)
class GoogleReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "rating",
        "source_label",
        "reviewed_at",
        "is_featured",
        "display_order",
    )
    list_filter = ("is_featured", "rating", "source_label", "reviewed_at")
    search_fields = ("name", "review_text", "source_label")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "phone", "email", "address", "message")
    readonly_fields = ("created_at", "updated_at")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("line_total",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_phone",
        "payment_method",
        "payment_status",
        "order_status",
        "total_amount",
        "created_at",
    )
    list_filter = ("payment_method", "payment_status", "order_status", "created_at")
    search_fields = ("customer_name", "customer_email", "customer_phone")
    readonly_fields = ("created_at", "updated_at", "total_amount")
    inlines = [OrderItemInline]
