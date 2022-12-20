from ..views.api.internments import *
from django.urls import path


urlpatterns = [
    # GET
    path('activity-log/', activity_log_api),

    # POST
    path('register-internments/', register_internment_api),
    path('add-log/', add_activity_log_api),

    # PUT
]
