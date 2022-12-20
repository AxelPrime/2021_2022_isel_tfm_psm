from ..models import MedicalInstitution
from django.contrib import admin


@admin.register(MedicalInstitution)
class MedicalInstitutionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "nif",
        "institution_code"
    ]

    search_fields = [
        "name",
        "nif",
        "institution_code"
    ]
