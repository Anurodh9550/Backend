import secrets

from django.conf import settings
from rest_framework.permissions import BasePermission


class HasAdminApiKey(BasePermission):
    """
    Simple API key guard for admin operations.
    Send header: X-Admin-Api-Key: <key>
    """

    message = "Admin API key is missing or invalid."

    def has_permission(self, request, view):
        configured_key = (getattr(settings, "ADMIN_API_KEY", "") or "").strip()
        # Local dev convenience: if API key is not configured, allow access in DEBUG.
        if not configured_key and getattr(settings, "DEBUG", False):
            return True
        if not configured_key:
            return False
        provided_key = (request.headers.get("X-Admin-Api-Key", "") or "").strip()
        if not provided_key:
            return False
        return secrets.compare_digest(provided_key, configured_key)
