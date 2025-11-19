from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import RecipientForm
from mailing.models import Recipient, Message, Mailing, LogMailing


class HomeListView(ListView):
    """Контроллер для стартовой страницы"""

    model = Recipient
    template_name = "home_page.html"


class CreateRecipientView(CreateView):
    """Контроллер для страницы создание получателя"""

    model = Recipient
    form_class = RecipientForm
    template_name = "create_recipient.html"
    success_url = reverse_lazy('mailing:home_page')

class ListRecipientView(ListView):
    """Контроллер для страницы со списком всех получателей рассылки"""

    model = Recipient
    template_name = "list_recipient.html"
    context_object_name = 'recipient'


class DetailRecipientView(DetailView):
    """Контроллер для страницы с подробной информацией о получателе рассылки"""

    model = Recipient


class UpdateRecipientView(UpdateView):
    """Контроллер для страницы изменения информации о получателе рассылки"""

    model = Recipient


class DeleteRecipientView(DeleteView):
    """Контроллер для страницы удаления получателя рассылки"""

    model = Recipient


class CreateMessageView(CreateView):
    """Контроллер для страницы создание сообщения"""

    model = Message


class ListMessageView(ListView):
    """Контроллер для страницы со списком всех сообщений"""

    model = Message


class DetailMessageView(DetailView):
    """Контроллер для страницы с подробной информацией об отдельном сообщении"""

    model = Message


class UpdateMessageView(UpdateView):
    """Контроллер для страницы изменения сообщения"""

    model = Message


class DeleteMessageView(DeleteView):
    """Контроллер для страницы удаления сообщения"""

    model = Message


class CreateMailingView(CreateView):
    """Контроллер для страницы создание рассылки"""

    model = Mailing


class ListMailingView(ListView):
    """Контроллер для страницы со списком всех рассылок"""

    model = Mailing


class DetailMailingView(DetailView):
    """Контроллер для страницы с подробной информацией о рассылке"""

    model = Mailing


class UpdateMailingView(UpdateView):
    """Контроллер для страницы изменения рассылки"""

    model = Mailing


class DeleteMailingView(DeleteView):
    """Контроллер для страницы удаления рассылки"""

    model = Mailing


class CreateLogMailingView(CreateView):
    """Контроллер для страницы создание логирования рассылки"""

    model = LogMailing


class ListLogMailingView(ListView):
    """Контроллер для страницы со списком всех логов всех рассылок"""

    model = LogMailing


class DetailLogMailingView(DetailView):
    """Контроллер для страницы с подробной информацией лога отдельной рассылки"""

    model = LogMailing


class UpdateLogMailingView(UpdateView):
    """Контроллер для страницы изменения настроек лога для рассылки"""

    model = LogMailing


class DeleteLogMailingView(DeleteView):
    """Контроллер для страницы удаления логирования рассылки"""

    model = LogMailing
