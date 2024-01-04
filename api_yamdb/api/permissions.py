from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the author of the object
        return obj.author == request.user


class IsModerator(IsAuthorOrReadOnly):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        # Moderators can edit or delete any object
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Admins and superusers have all permissions
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        # Admins and superusers can edit or delete any object
        return True
