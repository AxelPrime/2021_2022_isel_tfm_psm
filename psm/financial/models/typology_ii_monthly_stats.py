from django.db import models


class TypologyIIMonthlyStats(models.Model):
    # The months of the invoices.
    month_choices = [
        (1, "Janeiro"),
        (2, "Fevereiro"),
        (3, "Março"),
        (4, "Abril"),
        (5, "Maio"),
        (6, "Junho"),
        (7, "Julho"),
        (8, "Agosto"),
        (9, "Setembro"),
        (10, "Outubro"),
        (11, "Novembro"),
        (12, "Dezembro"),
    ]

    # The month of the stats.
    month = models.PositiveSmallIntegerField(choices=month_choices)
    # The year of the stats.
    year = models.IntegerField()
    # The total amount of money.
    total_amount = models.FloatField()
    # The total number of patients.
    total_patients = models.IntegerField()
    # The month's data.
    data = models.JSONField()

    def __str__(self):
        return f"{self.month}-{self.year}"
