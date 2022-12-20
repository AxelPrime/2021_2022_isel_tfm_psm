from entities.models import CareHouse
from financial.models import MonthlyInvoice
from internment_management.models import Referral
from .user import CustomUser
from django.db import models


class Notifications(models.Model):
    # The possible types of notifications.
    notification_type_choices = [
        ("referral_creation", "Criação de Referenciação"),
        ("referral_opening_indication", "Indicação de Vaga"),
        ("referral_evaluation", "Avaliação de Referenciação"),

        ("invoice_creation", "Criação de Recibo"),
        ("invoice_evaluation", "Avaliação de Recibo"),
    ]

    # The user types that can access this notification.
    user_type_choices = [
        ("doctor", "Institution Psychiatrist"),
        ("reviewer", "Referral Reviewer"),
        ("care_house_staff", "Care House Staff"),
        ("financial", "Financial Staff"),
    ]

    # The process that this refereal was created for.
    process_choices = [
        ("referral", "Referenciação"),
        ("invoice", "Recibo"),
    ]

    # The unique identifier for this notification.
    identifier = models.CharField(max_length=64, unique=True)
    # The type of notification.
    notification_type = models.CharField(max_length=27, choices=notification_type_choices)
    # The type of process that this notification was created for.
    process_type = models.CharField(choices=process_choices, max_length=8)
    # The user types that have access to this notification.
    user_type = models.CharField(choices=user_type_choices, max_length=16)

    # The care house that receives this notification (care house staff only)
    care_house = models.ForeignKey(CareHouse, on_delete=models.CASCADE, null=True, blank=True)
    # The referral that this notification was created for.
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE, null=True, blank=True)
    # The receipt that this notification was created for.
    receipt = models.ForeignKey(MonthlyInvoice, on_delete=models.CASCADE, null=True, blank=True)
    # The template that this notification is based on.
    template = models.ForeignKey("NotificationTemplate", on_delete=models.CASCADE)
    # Indicated if this notification is to be displayed.
    display = models.BooleanField(default=True)
    # Indicates if this notification is readable on click.
    readable_on_click = models.BooleanField(default=False)
    # The link to redirect the user to on click.
    redirect_to = models.CharField(max_length=256)

    # The date of creation of the notification.
    created = models.DateTimeField(auto_now_add=True)
    # The date of the last modification to this notification.
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_type
