from rest_framework.permissions import IsAuthenticated


class IsStaffUser(IsAuthenticated):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)