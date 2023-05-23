from rest_framework.permissions import BasePermission



class IsAuthenticatedOrNot(BasePermission) :

    def has_permission(self, request, view):
        return bool(request.user)
