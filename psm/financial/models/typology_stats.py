from django.db import models


class TypologyStats(models.Model):
    # The year of the stats.
    year = models.PositiveIntegerField()
    # The stats of by typology.
    typology_stats = models.JSONField()
    # The stats by care house.
    care_house_stats = models.JSONField()

    # The date of creation for the stats.
    created = models.DateTimeField(auto_now_add=True)
    # The date of the last modification to the data.
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.year)
