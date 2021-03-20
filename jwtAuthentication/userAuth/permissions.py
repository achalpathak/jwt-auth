from rest_framework.permissions import BasePermission


class IsTokenVerified(BasePermission):
    """
    Allows access only to users which have auth token.
    """

    def has_permission(self, request, view):
        if hasattr(request, 'user_details'):
            return True

        return False

class IsStaff(BasePermission):
    """
    Allows access to only staff users
    """

    def has_permission(self, request, view):
        if request.user_details.is_staff:
            return True

        return False