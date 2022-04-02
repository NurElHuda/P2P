from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return bool(request.user and obj.owner == request.user)


class IsManagerUser(permissions.BasePermission):
    """
    Global permission to only allow managers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and not request.user.is_anonymous and request.user.is_manager
        )


class IsAdminUser(permissions.BasePermission):
    """
    Global permission to only allow admins.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and not request.user.is_anonymous and request.user.is_admin
        )


class IsAgentUser(permissions.BasePermission):
    """
    Global permission to only allow agents.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and not request.user.is_anonymous and request.user.is_agent
        )


class IsTeacherUser(permissions.BasePermission):
    """
    Global permission to only allow teachers.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and not request.user.is_anonymous and request.user.is_teacher
        )


class IsStudentUser(permissions.BasePermission):
    """
    Global permission to only allow students.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and not request.user.is_anonymous and request.user.is_student
        )
