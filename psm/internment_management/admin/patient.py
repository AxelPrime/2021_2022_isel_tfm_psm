from django.contrib import admin
from ..models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sns_number",
        "social_security_number",
    ]

    search_fields = [
        "name",
        "sns_number",
        "social_security_number"
    ]
