from ..models import ActivityLog
from django.contrib import admin


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = [
        "internment",
        "executed_by",
        "action",
        "log_date",
    ]

    search_fields = [
        "internment__referral__patient__name",
        "executed_by__first_name",
        "executed_by__last_name",
    ]
