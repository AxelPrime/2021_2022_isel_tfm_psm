from django.contrib import admin
from ..models import TypologyStats
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(TypologyStats)
class TypologyStatsAdmin(admin.ModelAdmin):
    list_display = [
        "year"
    ]

    list_filter = [
        "year"
    ]

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
