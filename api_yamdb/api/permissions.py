from rest_framework import permissions

from users.constants import ADMIN, MODERATOR

from users.constants import ADMIN, MODERATOR

from users.constants import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrAdminOrModerator(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user == obj.author
            or request.user.role == MODERATOR
            or request.user.role == ADMIN
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )
