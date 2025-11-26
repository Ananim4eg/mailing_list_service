from django.core.exceptions import PermissionDenied


class OwnerCheckMixin:
    """Миксин для проверки, что текущий пользователь — владелец объекта."""

    def get_owner(self, obj):
        return obj.owner

    def get_object(self, queryset=None):

        obj = super().get_object(queryset)
        extra_data = getattr(self, 'extra_context', None)

        if self.request.user == self.get_owner(obj) or self.request.user.is_superuser or extra_data:
            return obj

        raise PermissionDenied("Вы не являетесь владельцем.")
