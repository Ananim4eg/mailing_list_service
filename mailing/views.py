from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.mixins import OwnerCheckMixin
from mailing.models import Recipient, Message, Mailing, LogMailing


class HomeListView(ListView):
    """Контроллер для стартовой страницы"""

    model = Recipient
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):

        quantity_uniq_recipients = Recipient.objects.all().distinct().count()
        quantity_mailings = Mailing.objects.all().count()
        quantity_starting_mailing = Mailing.objects.filter(status='started').count()

        context = {
            'quantity_uniq_recipients': quantity_uniq_recipients,
            'quantity_mailings': quantity_mailings,
            'quantity_starting_mailing': quantity_starting_mailing,
        }

        return context


class CreateRecipientView(CreateView):
    """Контроллер для страницы создание получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/create_recipient.html"
    success_url = reverse_lazy('mailing:home_page')

    def form_valid(self, form):
        """Добавляем текущего авторизованного пользователя как владельца при создании получателя"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ListRecipientView(LoginRequiredMixin, ListView):
    """Контроллер для страницы со списком всех получателей рассылки"""

    model = Recipient
    template_name = "recipient/list_recipient.html"
    context_object_name = 'recipients'


class DetailRecipientView(View):
    """Контроллер для страницы с подробной информацией о получателе рассылки"""

    def get(self, request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {
                'fullname': recipient.full_name,
                'email': recipient.email,
                'comment': recipient.comment,
                'urls':{
                    'url_1': reverse('mailing:update_recipient', kwargs={'pk': recipient.pk}),
                    'url_2': reverse('mailing:delete_recipient', kwargs={'pk': recipient.pk}),
                }
            }

            return JsonResponse(data)

        return render(request, 'recipient/detail_recipient.html', {'recipient': recipient})


class UpdateRecipientView(OwnerCheckMixin, UpdateView):
    """Контроллер для страницы изменения информации о получателе рассылки"""

    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/update_recipient.html"
    success_url = reverse_lazy('mailing:all_recipient')




class DeleteRecipientView(OwnerCheckMixin, DeleteView):
    """Контроллер для страницы удаления получателя рассылки"""

    model = Recipient
    template_name = 'recipient/delete_recipient.html'
    context_object_name = 'recipient'
    success_url = reverse_lazy('mailing:all_recipient')


class CreateMessageView(CreateView):
    """Контроллер для страницы создание сообщения"""

    model = Message
    form_class = MessageForm
    template_name = 'message/create_message.html'
    success_url = reverse_lazy('mailing:all_message')

    def form_valid(self, form):
        """Добавляем текущего авторизованного пользователя как владельца при создании сообщения"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ListMessageView(LoginRequiredMixin, ListView):
    """Контроллер для страницы со списком всех сообщений"""

    model = Message
    template_name = 'message/list_message.html'
    context_object_name = 'messages'


class DetailMessageView(OwnerCheckMixin, DetailView):
    """Контроллер для страницы с подробной информацией об отдельном сообщении"""

    model = Message
    form_class = MessageForm
    template_name = 'message/detail_message.html'
    context_object_name = 'message'


class UpdateMessageView(OwnerCheckMixin, UpdateView):
    """Контроллер для страницы изменения сообщения"""

    model = Message
    form_class = MessageForm
    template_name = 'message/update_message.html'
    context_object_name = 'message'

    def get_success_url(self):
        return reverse_lazy('mailing:detail_message', kwargs={'pk': self.object.pk})


class DeleteMessageView(OwnerCheckMixin, DeleteView):
    """Контроллер для страницы удаления сообщения"""

    model = Message
    template_name = 'message/delete_message.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing:all_message')


class CreateMailingView(CreateView):
    """Контроллер для страницы создание рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/create_mailing.html'
    success_url = reverse_lazy('mailing:all_mailing')

    def form_valid(self, form):
        """Добавляем текущего авторизованного пользователя как владельца при создании рассылки"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ListMailingView(LoginRequiredMixin, ListView):
    """Контроллер для страницы со списком всех рассылок"""

    model = Mailing
    template_name = 'mailing/list_mailing.html'
    context_object_name = 'mailings'


class ConfirmationSendMailingView(OwnerCheckMixin, DetailView):
    """Контроллер для страницы подтверждения отправки рассылки"""

    model = Mailing
    template_name = 'mailing/confirmation_send_mailing.html'


class SendEmailView(DetailView):
    """Контроллер для отправки писем"""

    model = Mailing

    def post(self, request, pk):
        mailing = self.get_object()

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
                return JsonResponse({
                    'status': 'error',
                    'message': 'Нет получателей для отправки!'
                })

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

                return redirect('mailing:success_page')

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
            messages.error(request, f"Ошибка: {str(e)}")
            return redirect('mailing:error_page')


class SuccessSendView(TemplateView):
    """Контроллер для успешной отправки"""

    template_name = 'mailing/success_page.html'


class ErrorSendView(TemplateView):
    """Контроллер для не успешной отправки"""

    template_name = 'mailing/error_page.html'


class DetailMailingView(OwnerCheckMixin, DetailView):
    """Контроллер для страницы с подробной информацией о рассылке"""

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/detail_mailing.html'
    context_object_name = 'mailing'


class UpdateMailingView(OwnerCheckMixin, UpdateView):
    """Контроллер для страницы изменения рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/update_mailing.html'
    context_object_name = 'mailing'

    def get_success_url(self):
        return reverse_lazy('mailing:detail_mailing', kwargs={'pk': self.object.pk})


class DeleteMailingView(OwnerCheckMixin, DeleteView):
    """Контроллер для страницы удаления рассылки"""

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/delete_mailing.html'
    context_object_name = 'mailing'
    success_url = reverse_lazy('mailing:all_mailing')


class ListLogMailingView(LoginRequiredMixin, ListView):
    """Контроллер для страницы со списком всех логов всех рассылок"""

    model = LogMailing
    template_name = 'log_mailing/list_log_mailing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mailings_with_logs = Mailing.objects.filter(logs__isnull=False).distinct()

        mailings_with_logs = mailings_with_logs.select_related('message')

        context['mailings'] = mailings_with_logs

        return context


class DetailLogMailingView(View):
    """Контроллер для страницы с информацией лога отдельной рассылки"""

    def get(self, request, pk):

        all_try = LogMailing.objects.filter(mailing=pk)
        all_success_try = all_try.filter(status='success').count()
        all_unsuccess_try = all_try.filter(status='unsuccess').count()
        success_rate = int(round((all_success_try / all_try.count()) * 100, 0))

        mailing = all_try.first().mailing
        mailing_name = f'id {mailing.pk} - {mailing.message.message_subject}'

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {
                'name': mailing_name,
                'all_try': all_try.count(),
                'all_success_try': all_success_try,
                'all_unsuccess_try': all_unsuccess_try,
                'success_rate': success_rate,
                'url': reverse('mailing:detail_info_mailing', kwargs={'pk': pk})
            }

            return JsonResponse(data)

        return HttpResponse('Ошибка получения данных о рассылке', status=400)


class DetailInfoLogMailingView(DetailView):
    """Контроллер для страницы с подробной информацией лога отдельной рассылки"""

    model = LogMailing
    template_name = 'log_mailing/detail_log_mailing.html'

    def get_context_data(self, **kwargs):

        all_try = LogMailing.objects.filter(mailing=self.kwargs['pk'])
        all_success_try = all_try.filter(status='success')
        all_unsuccess_try = all_try.filter(status='unsuccess')

        context ={
            'all_success_try': all_success_try,
            'all_unsuccess_try': all_unsuccess_try
        }

        return context


def my_message_403(request, exception=None):
    return render(
        request,
        '403.html',  # ваш шаблон
        {
            'message': 'У вас нет доступа к этому объекту.',
            'exception': 'Вы не являетесь владельцем'
        },
        status=403
    )
