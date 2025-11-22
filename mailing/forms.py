from django import forms

from mailing.models import Recipient, Message, Mailing, LogMailing


class RecipientForm(forms.ModelForm):
    """Форма для полей модели получателя"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите почту',
            'style': 'width: 600px;'
        })

        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ФИО',
            'style': 'width: 600px;'
        })

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите комментарий',
            'style': 'width: 600px;'
        })

    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):
    """Форма для полей модели сообщения"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['message_subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему сообщения',
            'style': 'width: 600px;'
        })

        self.fields['message_body'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите текст сообщения',
            'style': 'width: 600px;'
        })

    class Meta:
        model = Message
        fields = ['message_subject', 'message_body',]


class MailingForm(forms.ModelForm):
    """Форма для полей модели рассылки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['recipient'].widget.attrs.update({
            'class': 'form-select',
            'style': 'width: 600px;'
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-select',
            'style': 'width: 600px;'
        })

        self.fields['status'].widget.attrs.update({
            'class': 'form-select',
            'style': 'width: 150px;'
        })

    class Meta:
        model = Mailing
        fields = ['recipient', 'message','status',]


class LogMailingForm(forms.ModelForm):
    """Форма для полей модели логирования рассылки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mailing'].widget.attrs.update({
            'class': 'form-control',
            'style': 'width: 600px;'
        })

    class Meta:
        model = LogMailing
        fields = ['mailing',]
