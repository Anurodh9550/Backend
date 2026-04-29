from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminStatsView,
    CollectionViewSet,
    ContactSubmissionViewSet,
    GoogleReviewViewSet,
    ProductViewSet,
    SupportRequestViewSet,
    WarrantyClaimViewSet,
)

router = DefaultRouter()
router.register("collections", CollectionViewSet, basename="collection")
router.register("products", ProductViewSet, basename="product")
router.register("contact-submissions", ContactSubmissionViewSet, basename="contact")
router.register("warranty-claims", WarrantyClaimViewSet, basename="warranty-claim")
router.register("google-reviews", GoogleReviewViewSet, basename="google-review")
router.register("support-requests", SupportRequestViewSet, basename="support-request")

urlpatterns = [
    path("", include(router.urls)),
    path("admin-stats/", AdminStatsView.as_view(), name="admin-stats"),
]
