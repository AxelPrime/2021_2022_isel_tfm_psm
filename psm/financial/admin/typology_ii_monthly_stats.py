from ..models import TypologyIIMonthlyStats
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(TypologyIIMonthlyStats)
class TypologyIIMonthlyStatsAdmin(admin.ModelAdmin):
    list_display = [
        "year",
        "month",
        "total_amount",
        "total_patients"
    ]

    list_filter = [
        "year",
        "month"
    ]

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
