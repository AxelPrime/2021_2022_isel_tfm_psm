from django.db import models
from entities.models import CareHouse
from ..utils.invoice_files_path import invoice_files_path


class MonthlyInvoice(models.Model):
    # The possible status of the receipt.
    status_choices = [
        ('temp', 'Dados Temporários'),
        ('awaits_payment', 'Aguarda Pagamento'),
        ('paid', 'Pago'),
        ('rejected', 'Reprovado'),
    ]

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

    # The invoice's number.
    invoice_number = models.PositiveIntegerField(unique=True)
    # The care house that this invoice belongs to.
    care_house = models.ForeignKey(CareHouse, on_delete=models.CASCADE)
    # The typology.
    typology = models.CharField(max_length=3)
    # The lines of the invoice.
    invoice_lines = models.JSONField()
    # The start date of the invoice lines.
    start_date = models.DateField()
    # The end date of the invoice lines.
    end_date = models.DateField()
    # The month of the invoice.
    month = models.PositiveSmallIntegerField(choices=month_choices)
    # The year of the invoice.
    year = models.PositiveSmallIntegerField()
    # The file of the invoice.
    invoice_file = models.FileField(null=True, blank=True, upload_to=invoice_files_path)
    # The status of this invoice.
    status = models.CharField(max_length=15, choices=status_choices,)
    # The reason for this invoice to be rejected.
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return str({self.invoice_number})
