from rest_framework import serializers
from django.contrib.auth.models import User

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
    collection_description = serializers.CharField(
        source="collection.description", read_only=True
    )
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "collection",
            "collection_name",
            "collection_slug",
            "collection_description",
            "name",
            "slug",
            "short_description",
            "product_features",
            "category",
            "chair_type",
            "badge_label",
            "image",
            "hover_image",
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


class OrderItemSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "quantity",
            "unit_price",
            "line_total",
            "image_url",
        ]
        read_only_fields = ["line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "customer_phone",
            "shipping_address",
            "payment_method",
            "payment_status",
            "order_status",
            "total_amount",
            "gateway_transaction_id",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["total_amount", "created_at", "updated_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        total_amount = 0
        prepared_items = []
        for item_data in items_data:
            quantity = int(item_data.get("quantity", 1) or 1)
            unit_price = item_data.get("unit_price", 0)
            line_total = unit_price * quantity
            total_amount += line_total
            item_data["quantity"] = quantity
            item_data["line_total"] = line_total
            prepared_items.append(item_data)

        order = Order.objects.create(total_amount=total_amount, **validated_data)
        for item_data in prepared_items:
            OrderItem.objects.create(order=order, **item_data)
        return order


class UserPublicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "email", "date_joined"]

    def get_name(self, obj: User) -> str:
        full_name = obj.get_full_name().strip()
        return full_name or obj.first_name or obj.username


class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_email(self, value: str) -> str:
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already registered.")
        return email

    def create(self, validated_data):
        email = validated_data["email"]
        name = validated_data["name"].strip()
        password = validated_data["password"]
        username = email
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=6, write_only=True)
    confirm_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ["Passwords do not match."]}
            )
        return attrs
