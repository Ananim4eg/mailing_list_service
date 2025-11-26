from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from users.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    def __init__(self, *args, **kwargs):
        super(CustomUserCreateForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите почтовый адрес',
            'style': 'width: 450px;'
        })

        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
            'aria-label': 'Загрузить аватар',
            'style': 'width: 450px;'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'style': 'width: 450px;'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'style': 'width: 450px;'
        })

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "avatar", "password1", "password2")


class CustomUserLogin(AuthenticationForm):
    """Форма авторизации пользователя"""

    def __init__(self, *args, **kwargs):
        super(CustomUserLogin, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите почту',
            'style': 'width: 300px;'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'style': 'width: 300px;'
        })


class ProfileForm(forms.ModelForm):
    """Форма для полей модели сообщения"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
            'style': 'width: 450px;'
        })

        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
            'style': 'width: 450px;'
        })

        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите номер телефона',
            'style': 'width: 450px;'
        })

        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите страну проживания',
            'style': 'width: 450px;'
        })

    class Meta:
        model = CustomUser
        fields = ['email', 'avatar', 'phone_number', 'country', 'is_active']


class ResetPasswordForm(PasswordResetForm):
    """Форма для сброса пароля"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите адрес электронной почты',
            'style': 'width: 450px;'
        })

    class Meta:
        model = CustomUser
        fields = ['email',]


class SelectPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(user, *args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите новый пароль',
            'style': 'width: 450px;'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'style': 'width: 450px;'
        })
