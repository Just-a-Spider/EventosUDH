from rest_framework.permissions import BasePermission
from user.models import Coordinator

class IsCoordinator(BasePermission):
    """
    Custom permission to only allow coordinators to access the view.
    """
    def has_permission(self, request, view):
        return isinstance(request.user, Coordinator)