from importlib.resources import path
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("registration", registration),
    path("status",status),
    path("filter",filter),
    path("schedule",interviewSchedule),
    path("schedules",filterSchedule),
    path("mails",historyMails)
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)