from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'retrieve':
            return request.method in permissions.SAFE_METHODS
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class IsAdminUserOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            (request.user.is_staff or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            (request.user.is_staff or request.user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс ограничения прав пользователя."""

    def has_permission(self, request, view):
        """Возвращает True если пользователь admin или безопасный метод."""
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        """Возвращает True если пользователь admin"""
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return request.user.role == 'admin'
