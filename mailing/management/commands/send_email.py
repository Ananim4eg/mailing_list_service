from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from mailing.models import LogMailing, Mailing


class Command(BaseCommand):
    """Команда отправки рассылки"""

    help = 'Отправка письма'

    def add_arguments(self, parser):
        parser.add_argument('id_mailing', type=int, help='id нужной рассылки')

    def handle(self, *args, **options):
        mailing = Mailing.objects.filter(pk=options['id_mailing']).first()

        success_count = 0
        failed_emails = []

        if mailing.status != 'started':
            mailing.status = 'started'
            mailing.save()

        try:
            subject = mailing.message.message_subject
            message_body = mailing.message.message_body
            recipient_list = mailing.recipient.all()

            if not recipient_list:
                return self.stdout.write(self.style.ERROR('Нет получателей для отправки'))

            for recipient in recipient_list:
                try:
                    send_mail(
                        subject=subject,
                        message=message_body,
                        from_email='new.mail.test@mail.ru',
                        recipient_list=[recipient.email],
                        fail_silently=False
                    )
                    success_count += 1

                except Exception:
                    failed_emails.append(recipient.email)

            if len(failed_emails) == 0:
                LogMailing.objects.create(
                    mailing=mailing,
                    run_time=timezone.now(),
                    status='success',
                    server_answer=f'Отправлено {success_count} писем'
                )

                return self.stdout.write(self.style.SUCCESS('Рассылка отправлена всем получателям'))
            else:
                error_msg = f'Не удалось отправить на {len(failed_emails)} адресов: {", ".join(failed_emails)}'
                LogMailing.objects.create(
                    mailing=mailing,
                    run_time=timezone.now(),
                    status='unsuccess',
                    server_answer=error_msg
                )
                raise Exception(error_msg)

        except Exception as e:

            LogMailing.objects.create(
                mailing=mailing,
                run_time=timezone.now(),
                status='unsuccess',
                server_answer=f'error: {str(e)}'
            )
            return self.stdout.write(self.style.ERROR(f'Возникла ошибка при отправке рассылки: {e}'))
