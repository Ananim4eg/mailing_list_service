from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import CreateRecipientView, ListRecipientView, UpdateRecipientView, DetailRecipientView, \
    DeleteRecipientView, HomeListView, ListMessageView, CreateMessageView, UpdateMessageView, DetailMessageView, \
    DeleteMessageView, DeleteMailingView, DetailMailingView, UpdateMailingView, CreateMailingView, ListMailingView, \
    DetailLogMailingView, ListLogMailingView, ConfirmationSendMailingView, SendEmailView, SuccessSendView, \
    ErrorSendView, DetailInfoLogMailingView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home_page'),

    path('recipient/', ListRecipientView.as_view(), name='all_recipient'),
    path('recipient/create/', CreateRecipientView.as_view(), name='create_recipient'),
    path('recipient/update/<int:pk>/', UpdateRecipientView.as_view(), name='update_recipient'),
    path('recipient/detail/<int:pk>/', DetailRecipientView.as_view(), name='detail_recipient'),
    path('recipient/delete/<int:pk>/', DeleteRecipientView.as_view(), name='delete_recipient'),

    path('message/', ListMessageView.as_view(), name='all_message'),
    path('message/create/', CreateMessageView.as_view(), name='create_message'),
    path('message/update/<int:pk>/', UpdateMessageView.as_view(), name='update_message'),
    path('message/detail/<int:pk>/', DetailMessageView.as_view(), name='detail_message'),
    path('message/delete/<int:pk>/', DeleteMessageView.as_view(), name='delete_message'),

    path('mailing/', ListMailingView.as_view(), name='all_mailing'),
    path('mailing/create/', CreateMailingView.as_view(), name='create_mailing'),
    path('mailing/update/<int:pk>/', UpdateMailingView.as_view(), name='update_mailing'),
    path('mailing/detail/<int:pk>/', DetailMailingView.as_view(), name='detail_mailing'),
    path('mailing/delete/<int:pk>/', DeleteMailingView.as_view(), name='delete_mailing'),
    path('mailing/confirmation/<int:pk>/', ConfirmationSendMailingView.as_view(), name='confirmation_mailing'),
    path('mailing/send/<int:pk>/', SendEmailView.as_view(), name='send_mailing'),
    path('mailing/success/', SuccessSendView.as_view(), name='success_page'),
    path('mailing/error/', ErrorSendView.as_view(), name='error_page'),

    path('log_mailing/', ListLogMailingView.as_view(), name='all_log_mailing'),
    path('log_mailing/detail/<int:pk>/', DetailLogMailingView.as_view(), name='detail_log_mailing'),
    path('log_mailing/detail/info/<int:pk>/', DetailInfoLogMailingView.as_view(), name='detail_info_mailing'),
]