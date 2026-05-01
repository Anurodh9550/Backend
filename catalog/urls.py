from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminStatsView,
    CollectionViewSet,
    ContactSubmissionViewSet,
    ForgotPasswordView,
    GoogleReviewViewSet,
    LoginUserView,
    OrderViewSet,
    ProductViewSet,
    RegisterUserView,
    SupportRequestViewSet,
    UserViewSet,
    WarrantyClaimViewSet,
)

router = DefaultRouter()
router.register("collections", CollectionViewSet, basename="collection")
router.register("products", ProductViewSet, basename="product")
router.register("contact-submissions", ContactSubmissionViewSet, basename="contact")
router.register("warranty-claims", WarrantyClaimViewSet, basename="warranty-claim")
router.register("google-reviews", GoogleReviewViewSet, basename="google-review")
router.register("support-requests", SupportRequestViewSet, basename="support-request")
router.register("users", UserViewSet, basename="users")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
    path("admin-stats/", AdminStatsView.as_view(), name="admin-stats"),
    path("auth/register/", RegisterUserView.as_view(), name="auth-register"),
    path("auth/login/", LoginUserView.as_view(), name="auth-login"),
    path("auth/forgot-password/", ForgotPasswordView.as_view(), name="auth-forgot-password"),
]
