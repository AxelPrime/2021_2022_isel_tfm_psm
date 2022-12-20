from django.db import models


class YearlyInvoice(models.Model):
    # The invoice number.
    invoice_number = models.PositiveIntegerField(unique=True)
    # the year of the invoice.
    year = models.PositiveIntegerField()
    # The total amount of the invoice.
    total_amount = models.FloatField()
    # The data of the invoice.
    data = models.JSONField()

    def __str__(self):
        return str(self.invoice_number)
