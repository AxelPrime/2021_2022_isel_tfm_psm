from django.contrib import admin
from ..models import DailyValue


@admin.register(DailyValue)
class DailyValueAdmin(admin.ModelAdmin):
    list_display = [
        'value',
        'start_date',
        'end_date'
    ]
