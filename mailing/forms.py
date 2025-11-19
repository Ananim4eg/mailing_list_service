from django import forms

from mailing.models import Recipient


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

