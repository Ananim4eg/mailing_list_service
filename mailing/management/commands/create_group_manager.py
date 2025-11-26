from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу "manager"'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Пересоздать группу, даже если она уже существует'
        )

    def handle(self, *args, **options):
        group_name = 'manager'

        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана.'))
        elif options['force']:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" будет обновлена.'))
            group.permissions.clear()
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Группа "{group_name}" уже существует. Используйте --force для обновления прав.'
                )
            )
            return
        desired_permissions = [
            'mailing.view_recipient',
            'users.view_customuser',
            'users.can_disable_user',
            'mailing.can_disable_mailing',
            'mailing.view_mailing',
            'mailing.view_message',
        ]

        for perm_codename in desired_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename.split('.')[1],
                                                    content_type__app_label=perm_codename.split('.')[0])
                group.permissions.add(permission)
                self.stdout.write(f'Право "{perm_codename}" добавлено группе.')
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Право "{perm_codename}" не найдено в базе данных.')
                )

        self.stdout.write(self.style.SUCCESS('Команда выполнена успешно.'))
