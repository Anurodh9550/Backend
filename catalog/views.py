from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Collection,
    ContactSubmission,
    GoogleReview,
    Product,
    SupportRequest,
    WarrantyClaim,
)
from .serializers import (
    CollectionSerializer,
    ContactSubmissionSerializer,
    GoogleReviewSerializer,
    ProductSerializer,
    SupportRequestSerializer,
    WarrantyClaimSerializer,
)
from .permissions import HasAdminApiKey


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "created_at", "updated_at"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [HasAdminApiKey()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "slug", "collection__name"]
    ordering_fields = ["price", "created_at", "updated_at", "home_order"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [HasAdminApiKey()]

    def get_queryset(self):
        queryset = super().get_queryset()
        collection_slug = self.request.query_params.get("collection")
        if collection_slug:
            queryset = queryset.filter(collection__slug=collection_slug)
        return queryset


class ContactSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "email", "phone", "comment"]
    ordering_fields = ["created_at", "updated_at", "status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [HasAdminApiKey()]


class WarrantyClaimViewSet(viewsets.ModelViewSet):
    queryset = WarrantyClaim.objects.all()
    serializer_class = WarrantyClaimSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["customer_name", "email", "phone", "product_name", "issue"]
    ordering_fields = ["created_at", "updated_at", "purchase_date", "status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [HasAdminApiKey()]


class GoogleReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoogleReview.objects.filter(is_featured=True)
    serializer_class = GoogleReviewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "review_text", "source_label"]
    ordering_fields = ["display_order", "created_at", "rating", "reviewed_at"]
    ordering = ["display_order", "-created_at"]


class SupportRequestViewSet(viewsets.ModelViewSet):
    queryset = SupportRequest.objects.all()
    serializer_class = SupportRequestSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["full_name", "phone", "email", "address", "message"]
    ordering_fields = ["created_at", "updated_at", "status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [HasAdminApiKey()]


class AdminStatsView(APIView):
    permission_classes = [HasAdminApiKey]

    def get(self, request):
        return Response(
            {
                "collections": Collection.objects.count(),
                "products": Product.objects.count(),
                "in_stock_products": Product.objects.filter(in_stock=True).count(),
                "out_of_stock_products": Product.objects.filter(in_stock=False).count(),
                "contact_submissions": ContactSubmission.objects.count(),
                "new_contacts": ContactSubmission.objects.filter(status="new").count(),
                "warranty_claims": WarrantyClaim.objects.count(),
                "open_warranty_claims": WarrantyClaim.objects.exclude(
                    status="closed"
                ).count(),
                "support_requests": SupportRequest.objects.count(),
                "open_support_requests": SupportRequest.objects.exclude(
                    status="closed"
                ).count(),
            }
        )
