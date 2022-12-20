from ..views.render import *
from django.urls import path


urlpatterns = [
    # Doctor
    path('doctor/active-referrals/', active_referrals),

    # Care House
    path('care-house/pending-referrals/', care_house_pending_referrals),
    path('care-house/pending-internments/', pending_internments),
    path('care-house/active-internments/', active_internments_page),
    path('care-house/internment-history/', internment_history_page),

    # Reviewer
    path('reviewer/active-referrals/', reviewer_pending_referrals),

    # superuser
    path('superuser/doctor/referrals/', superuser_doctor_referrals_page),
    path('superuser/care-house/referrals/', superuser_care_house_pending_referrals),
    path('superuser/reviewer/referrals/', superuser_reviewer_pending_referrals),
    path('superuser/care-house/pending-internments/', pending_internments),
    path('superuser/care-house/active-internments/', active_internments_page),
    path('superuser/care-house/internment-history/', internment_history_page),

    # General
    path('referrals/history/', referral_history)
]
