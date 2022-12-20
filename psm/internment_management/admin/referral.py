from django.contrib import admin
from ..models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "origin_institution",
        "care_house",
        "typology",
        "referral_date",
        "approval_date"
    ]

    search_fields = [
        "patient__name",
        "origin_institution__name",
        "care_house__name"
    ]

    list_filter = [
        "typology",
    ]