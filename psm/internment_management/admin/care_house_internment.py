from ..models import CareHouseInternment
from django.contrib import admin


@admin.register(CareHouseInternment)
class CareHouseInternmentAdmin(admin.ModelAdmin):
    list_display = [
        "referral",
        # "care_house",
        "admission_date",
        "admitted_by",
        "current_status",
    ]

    list_filter = [
        # "care_house",
    ]

    search_fields = [
        "referral__patient__name",
        "admitted_by__first_name",
        "admitted_by__last_name",
    ]
