from django.core.exceptions import PermissionDenied


class OwnerCheckMixin:
    """Миксин для проверки, что текущий пользователь — владелец объекта."""

    def get_owner(self, obj):
        return obj.owner

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == self.get_owner(obj):
            return obj
        raise PermissionDenied("У вас нет доступа к этому объекту.")
