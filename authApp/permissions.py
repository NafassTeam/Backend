from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

class IsAdminOrSelfPatient(BasePermission):
    def has_permission(self, request, view):
        # Allow access if the user is an admin or staff
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Allow patients to perform actions on their own data
        if request.user.role == 'patient':
            # For read (GET) requests or modifying (PUT/PATCH/DELETE) their own data
            if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
                return True
        
        # Deny any other actions
        return False

    def has_object_permission(self, request, view, obj):
        # If the request is GET/PUT/PATCH/DELETE, ensure it's the patient's own data
        if request.user.is_superuser or request.user.is_staff:
            return True
        return obj.user == request.user



class IsAdminOrSelfTherapist(BasePermission):
    def has_permission(self, request, view):
        # Allow access if the user is an admin or staff
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Allow therapists to perform actions on their own data
        if request.user.role == 'therapist':
            # For read (GET) requests or modifying (PUT/PATCH/DELETE) their own data
            if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
                return True
        
        # Deny any other actions
        return False

    def has_object_permission(self, request, view, obj):
        # If the request is GET/PUT/PATCH/DELETE, ensure it's the therapit's own data
        if request.user.is_superuser or request.user.is_staff:
            return True
        return obj.user == request.user

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff