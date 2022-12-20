from ..models import MonthlyInvoice
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(MonthlyInvoice)
class MonthlyInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number",
        "care_house",
        "typology",
        "start_date",
        "end_date",
        "status"
    ]

    search_fields = [
        "invoice_number",
    ]

    list_filter = [
        "care_house",
        "typology",
        "status"
    ]

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
