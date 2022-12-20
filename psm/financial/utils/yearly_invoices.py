from random import randint

from financial.models import YearlyInvoice, MonthlyInvoice


def update_yearly_invoice(monthly_invoice: MonthlyInvoice):
    # Obtain the yearly_invoice.
    try:
        yearly_incoice = YearlyInvoice.objects.get(year=monthly_invoice.year)
    except YearlyInvoice.DoesNotExist:
        yearly_incoice = YearlyInvoice(
            year=monthly_invoice.year,
            invoice_number=randint(1, 100000),
            total_amount=0,
            data={
                'lines': []
            }
        )
        yearly_incoice.save()

    # Map the monthly invoice data to add to the yearly invoice.
    lines_to_add = list(map(
        lambda a: [
            a['patient_name'],
            monthly_invoice.get_month_display(),
            a['invoice_start'],
            a['invoice_end'],
            a['total_days'],
            a['total_amount'],
            f'<a href="javascript:void(0);" data-referral-id="{a["referral_id"]}" onclick="Referrals.getReferralDetails(this)">Ver Detalhes</a>'
        ],
        monthly_invoice.invoice_lines['data']
    ))

    # Add the lines to the invoice.
    yearly_incoice.data['lines'].extend(lines_to_add)
    yearly_incoice.total_amount += monthly_invoice.invoice_lines['total_amount']

    # Save the invoice data.
    yearly_incoice.save()
