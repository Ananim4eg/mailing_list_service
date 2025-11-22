from django.contrib import admin

from mailing.models import Recipient, Message, Mailing, LogMailing


@admin.register(Recipient)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'comment', 'created_at', 'update_at']
    list_filter = ('full_name',)
    search_fields = ('email','full_name',)


@admin.register(Message)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_subject', 'message_body', 'created_at', 'update_at']
    list_filter = ('id', 'message_subject',)
    search_fields = ('message_subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id','first_message', 'stop_mailing', 'status', 'message', 'recipient', 'created_at', 'update_at']

    def recipient(self, obj):
        return ", ".join([c.name for c in obj.recipient.all()])

    recipient.short_description = "Получатели"

    list_filter = ('id', 'status',)
    search_fields = ('id', 'recipient')



@admin.register(LogMailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'run_time', 'status', 'server_answer', 'mailing', 'created_at', 'update_at']

    list_filter = ('status', 'mailing',)
    search_fields = ('id', 'mailing')
