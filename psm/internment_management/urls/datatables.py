from ..views.api.datatables import *
from django.urls import path


urlpatterns = [
    # GET
    path('internments/awaits-entrance/', patients_await_entrance_api),
    path('internments/active/', active_internments_api),
    path('internments/history/', internment_history_api),
    path('referrals/active/', referred_patients_api),
    path('referrals/awaits-opening/', awaits_opening_api),
    path('referrals/awaits-approval/', awaits_approval_api),
    path('referrals/history/', referrals_history_api),

    # POST

    # PUT
]