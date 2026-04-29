from rest_framework import serializers

from .models import (
    Collection,
    ContactSubmission,
    GoogleReview,
    Product,
    SupportRequest,
    WarrantyClaim,
)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "banner_image",
            "created_at",
            "updated_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    collection_name = serializers.CharField(source="collection.name", read_only=True)
    collection_slug = serializers.CharField(source="collection.slug", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "collection",
            "collection_name",
            "collection_slug",
            "name",
            "slug",
            "short_description",
            "product_features",
            "image",
            "image_file",
            "image_url",
            "price",
            "old_price",
            "in_stock",
            "show_on_home",
            "home_order",
            "created_at",
            "updated_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image_file:
            url = obj.image_file.url
            return request.build_absolute_uri(url) if request else url
        return obj.image


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "comment",
            "status",
            "created_at",
            "updated_at",
        ]


class WarrantyClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarrantyClaim
        fields = [
            "id",
            "customer_name",
            "email",
            "phone",
            "product_name",
            "purchase_date",
            "issue",
            "status",
            "created_at",
            "updated_at",
        ]


class GoogleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleReview
        fields = [
            "id",
            "name",
            "review_text",
            "rating",
            "source_label",
            "source_url",
            "reviewed_at",
            "is_featured",
            "display_order",
            "created_at",
            "updated_at",
        ]


class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "address",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]
