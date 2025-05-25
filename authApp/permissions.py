from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminOrSelfPatient(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True

    # Only allow 'me' action for regular patients
        if view.action == 'me':
            return True

        return False



class IsAdminOrSelfTherapist(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True

    # Only allow 'me' action for regular therapists:
        if view.action == 'me':
            return True

        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff