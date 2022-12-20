from ..models import CareHouse
from django.contrib import admin


@admin.register(CareHouse)
class CareHouseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "identification_code"
    ]

    search_fields = [
        "name"
    ]
