from rest_framework.permissions import BasePermission, SAFE_METHODS

class OwnerCanManageReadOnly(BasePermission):
    message = ''

    def has_object_permission(self, request, view):
        self.message = 'تو باید  ادمین باشی تا بتونی ادیتش کنی باهوش '
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_anonymous:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        self.message = 'این پست تو نیست که بتونی ادیتش کنی متاسفم'
        return request.user == obj.owner