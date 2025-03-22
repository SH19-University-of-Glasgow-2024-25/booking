from rest_framework.permissions import BasePermission

# Based on https://stackoverflow.com/a/31275034, CC BY-SA 3.0
class IsAuthenticatedOrOptions(BasePermission):
    """
    The request is authenticated as a user, or an OPTIONS request.
    """

    def has_permission(self, request, view):
        return (
            request.method == 'OPTIONS' or request.user and request.user.is_authenticated
        )