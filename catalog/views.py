from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import (
    Collection,
    ContactSubmission,
    GoogleReview,
    Order,
    Product,
    SupportRequest,
    WarrantyClaim,
)
from .serializers import (
    CollectionSerializer,
    ContactSubmissionSerializer,
    ForgotPasswordSerializer,
    GoogleReviewSerializer,
    OrderSerializer,
    ProductSerializer,
    SupportRequestSerializer,
    UserLoginSerializer,
    UserPublicSerializer,
    UserRegistrationSerializer,
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
    search_fields = ["name", "slug", "collection__name", "category", "chair_type"]
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
    serializer_class = GoogleReviewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "review_text", "source_label"]
    ordering_fields = ["display_order", "created_at", "rating", "reviewed_at"]
    ordering = ["display_order", "-created_at"]

    def get_queryset(self):
        # Home page: default = featured only. Full list: ?all=1
        qs = GoogleReview.objects.all()
        if self.request.query_params.get("all") == "1":
            return qs
        return qs.filter(is_featured=True)


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["customer_name", "customer_email", "customer_phone", "items__product_name"]
    ordering_fields = ["created_at", "updated_at", "total_amount", "payment_status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [HasAdminApiKey()]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserPublicSerializer

    def get_permissions(self):
        return [HasAdminApiKey()]


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserPublicSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user is None:
            existing = User.objects.filter(email__iexact=email).first()
            if existing:
                user = authenticate(request, username=existing.username, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(UserPublicSerializer(user).data)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            return Response(
                {"detail": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response({"detail": "Password reset successful."})


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
                "users": User.objects.count(),
                "orders": Order.objects.count(),
                "paid_orders": Order.objects.filter(payment_status="paid").count(),
                "pending_payments": Order.objects.filter(payment_status="pending").count(),
            }
        )
