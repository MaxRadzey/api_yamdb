from rest_framework import permissions

from users.constants import MODERATOR, ADMIN


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsModerator(IsAuthorOrReadOnly):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return True


class IsAuthorOrAdminOrModerator(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user == obj.author
            or request.user.role == MODERATOR
            or request.user.role == ADMIN
        )
