from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # TODO
        course_id = view.kwargs.get("course_id")

        access = Subscription.objects.filter(
            user=request.user, course_id=course_id).exists()
        return access or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # TODO
        course_id = view.kwargs.get("course_id")

        access = Subscription.objects.filter(
            user=request.user, course_id=course_id).exists()

        return access or request.user.is_staff


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
