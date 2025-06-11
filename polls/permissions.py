from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only read.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in ['GET','HEAD','OPTIONS'] or obj.created_by == request.user