from ..views.api.stats import *
from django.urls import path


urlpatterns = [
    # GET
    path('typology/', typology_stats_api),
    path('typology-ii/stats/', typology_ii_stats_api),
    path('care-house/', care_house_stats_api),
    path('typology/download/', download_typology_stats_api),
    path('care-house/download/', download_care_house_stats_api),
    path('typology-ii/stats/download/', download_tip_ii_api),

    # POST
    path('daily-value/add/', add_daily_value_api),

    # PUT
]
