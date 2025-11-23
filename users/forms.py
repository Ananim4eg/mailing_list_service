from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите почту',
            'style': 'width: 300px;'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'style': 'width: 300px;'
        })
