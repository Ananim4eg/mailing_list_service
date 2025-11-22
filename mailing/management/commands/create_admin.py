from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Создает суперпользователя в БД"""

    def handle(self, *args, **options):

        User = get_user_model()
        user = User.objects.create(
            email='new.mail.test@mail.ru',
            first_name='Admin',
            last_name='Adminex'
        )
        user.set_password('Admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Успешно создан суперпользователь с email {user.email}'))
