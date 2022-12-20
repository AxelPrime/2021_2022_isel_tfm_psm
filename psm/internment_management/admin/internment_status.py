from ..models import InternmentStatus
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


@admin.register(InternmentStatus)
class InternmentStatusAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = [
        "name",
        "label"
    ]

    search_fields = [
        "name",
        "label"
    ]
