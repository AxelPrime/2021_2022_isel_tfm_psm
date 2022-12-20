from django.contrib import admin
from ..models import NotificationTemplate


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "identifier"
    ]

    search_fields = [
        "identifier"
    ]
