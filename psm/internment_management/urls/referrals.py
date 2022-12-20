from ..views.api.referrals import *
from django.urls import path


urlpatterns = [
    # GET
    path('details/', get_referral_details_api),
    path('patient-data/', patient_data_api),
    path('responsibility-term/', download_responsibility_term_api),
    path('supervision-scale/', download_supervision_scale_api),

    # POST
    path('refer-patient/', refer_patient_api),
    path('evaluate/', evaluate_referral_api),

    # PUT
]