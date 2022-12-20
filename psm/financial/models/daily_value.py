from django.db import models


class DailyValue(models.Model):
    # The value to be accounted.
    value = models.FloatField()
    # The start date to apply the value.
    start_date = models.DateField()
    # The end date to apply the value.
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.value)
