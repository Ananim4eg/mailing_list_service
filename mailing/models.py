from django.db import models


class Recipient(models.Model):
    """Модель получателя рассылки"""

    email = models.EmailField(unique=True, verbose_name='Почта получателя')
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['email']


class Message(models.Model):
    """Модель сообщения"""

    message_subject = models.CharField(max_length=50, verbose_name='Тема письма')
    message_body = models.TextField(verbose_name='Тело письма')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.message_subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['message_subject']


class Mailing(models.Model):
    """Модель рассылки"""

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('stoped', 'Завершена'),
    ]

    first_message = models.DateTimeField(verbose_name='Дата первого сообщения', null=True, blank=True)
    stop_mailing = models.DateTimeField(verbose_name='Дата окончания рассылки', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipient = models.ManyToManyField(Recipient, related_name='mailings')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.message} - {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['status']


class LogMailing(models.Model):
    """Модель логирования попыток рассылки"""

    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('unsuccess', 'Не успешно'),
    ]

    run_time = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='Статус отправки')
    server_answer = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.mailing} - {self.status}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
        ordering = ['status']
