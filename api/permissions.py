from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthorOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class AdminOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class ReviewCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
        )