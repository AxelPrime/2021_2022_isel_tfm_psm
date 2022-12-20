from django.db import models
from user_management.models import CustomUser
from .care_house_internment import CareHouseInternment


class ActivityLog(models.Model):
    # The possible types of activity.
    activity_type_choices = [
        ('entry', 'Entrada'),
        ('temporary_leave', 'Saída Temporária'),
        ('return', 'Retorno'),
        ('exit', 'Saída')
    ]

    # The identifier of the log.
    identifier = models.CharField(max_length=64, unique=True)
    # The Internment that this log belongs to.
    internment = models.ForeignKey(CareHouseInternment, on_delete=models.CASCADE)
    # The user who created the activity log.
    executed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # The type of activity.
    activity_type = models.CharField(choices=activity_type_choices, max_length=15)
    # The action that has taken place.
    action = models.CharField(max_length=25)
    # The description of the log.
    description = models.TextField(blank=True)
    # the date of the activity.
    log_date = models.DateTimeField()

    def __str__(self):
        return self.action
