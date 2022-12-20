from financial.models import MonthlyInvoice, TypologyIIMonthlyStats
from internment_management.models import Referral


def update_typology_ii_stats(invoice: MonthlyInvoice):
    # Obtain the stats.
    try:
        stats = TypologyIIMonthlyStats.objects.get(year=invoice.year, month=invoice.month)
    except TypologyIIMonthlyStats.DoesNotExist:
        stats = TypologyIIMonthlyStats(
            year=invoice.year,
            month=invoice.month,
            total_amount=0,
            total_patients=0,
            data={
                'institutions': {}
            }
        )
        stats.save()

    # Get the referral identifiers.
    ref_ids = [
        line['referral_id']
        for line in invoice.invoice_lines['data']
    ]
    # Get the invoice referrals.
    referrals = Referral.objects.select_related('origin_institution').filter(identifier__in=ref_ids)
    # Create the object holding the current invoice data.
    curr_invoice_data = stats.data['institutions']
    for ref in referrals:
        key = ref.origin_institution.institution_code
        curr_line = curr_invoice_data.get(key, {
            "name": ref.origin_institution.name,
            "nif": ref.origin_institution.nif,
            "data": {
                "amount": 0,
                "total_patients": 0
            }
        })

        line_amount = [
            invoice_line['total_amount']
            for invoice_line in invoice.invoice_lines['data'] if invoice_line['referral_id'] == ref.identifier
        ][0]

        curr_line['data']['amount'] += line_amount
        curr_line['data']['total_patients'] += 1

        stats.total_amount += line_amount
        stats.total_patients += 1

        curr_invoice_data[key] = curr_line

    stats.data['institutions'] = curr_invoice_data
    stats.save()
