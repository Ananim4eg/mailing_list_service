from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mailing.views import my_message_403

handler403 = my_message_403

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mailing/", include('mailing.urls', namespace='mailing')),
    path('users/', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

