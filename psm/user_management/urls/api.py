from django.urls import path

from ..views.api import *


urlpatterns = [
    # GET
    path('notifications/', user_notifications_api),

    # POST
    path('login/', login_api),
    path('logout/', logout_api),

    path("notifications/read/", read_notification_api)
]
