
# ✅ permissions.py
from rest_framework import permissions

class IsEmailVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_email_verified


# ✅ throttles.py
from rest_framework.throttling import SimpleRateThrottle

class PasswordResetRateThrottle(SimpleRateThrottle):
    scope = 'password_reset'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
