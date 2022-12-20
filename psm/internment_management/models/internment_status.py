from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django_better_admin_arrayfield.models.fields import ArrayField


class InternmentStatus(models.Model):
    # The possible types of status.
    status_choices = [
        ("referral", "Referral"),
        ("internment", "Internment"),
    ]

    # The label of this status.
    label = models.CharField(max_length=25, unique=True)
    # The name of the status.
    name = models.CharField(max_length=50)
    # The type of status.
    type = models.CharField(max_length=10, choices=status_choices, default="referral")
    # The possible next states.
    next_states = ArrayField(null=True, blank=True, base_field=models.CharField(max_length=25))
    # The possible previous states.
    prev_states = ArrayField(null=True, blank=True, base_field=models.CharField(max_length=25))

    def __str__(self):
        return self.name
