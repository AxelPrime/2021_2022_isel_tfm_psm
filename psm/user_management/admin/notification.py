from django.contrib import admin
from ..models import Notifications


@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "notification_type",
        "process_type",
        "user_type",
        "display",
        "created",
        "modified"
    ]

    list_filter = [
        "notification_type",
        "process_type",
        "user_type",
        "display"
    ]

    readonly_fields = [
        "created",
        "modified"
    ]


