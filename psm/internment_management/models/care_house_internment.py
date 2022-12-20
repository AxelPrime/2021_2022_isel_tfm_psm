from django.db import models

from user_management.models import CustomUser
from .patient import Patient
from .referral import Referral
from entities.models import CareHouse
from .internment_status import InternmentStatus


class CareHouseInternment(models.Model):
    # The possible reasons of leave.
    leave_choices = []

    # The identifier of the internment.
    identifier = models.CharField(max_length=64, unique=True)
    # The referral of the internment.
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
    # The care house where the internment will take place.
    # care_house = models.ForeignKey(CareHouse, on_delete=models.CASCADE)
    # The date of admission.
    admission_date = models.DateTimeField(null=True, blank=True)
    # The user who admitted to the care house.
    admitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # The current status.
    current_status = models.ForeignKey(InternmentStatus, on_delete=models.CASCADE)
    # The date of the end of the internment.
    leave_date = models.DateTimeField(null=True, blank=True)
    # The patient's reason to leave.
    # reason_to_leave = models.CharField(max_length=25, choices=leave_choices)

    def __str__(self):
        return self.referral.patient.name
