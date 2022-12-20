from ..models import YearlyInvoice
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(YearlyInvoice)
class YearlyInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number",
        "year",
        "total_amount",
    ]

    list_filter = [
        "year"
    ]

    search_fields = [
        "invoice_number"
    ]

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
