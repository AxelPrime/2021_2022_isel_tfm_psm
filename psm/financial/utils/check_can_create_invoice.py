from datetime import date

import calendar
from dateutil.relativedelta import relativedelta

from financial.models import MonthlyInvoice
from .invoice_dates_encryption import DateEncryption


def check_can_create_invoice(typology_list, care_house):
    # Get the current date.
    current_date = date.today()
    current_month = current_date.month
    current_year = current_date.year

    # Define the possible status for invoices.
    active_status = ['temp', 'awaits_payment']

    # The data to return.
    next_invoices = {}
    # The list of cookies to set.
    cookies_to_set = []

    for t in typology_list:
        # The message to show.
        message = ''
        # Get the previous invoice.
        last_invoice = MonthlyInvoice.objects.filter(
            care_house=care_house,
            typology=t
        ).order_by('-id').first()

        # The Encryption library.
        date_encryption = DateEncryption()

        # Check if there are invoices already created.
        if last_invoice is None:
            last_month_date = current_date - relativedelta(months=1)
            date_range = calendar.monthrange(last_month_date.year, last_month_date.month)
            can_create = True
            next_invoice_start_date = date(year=last_month_date.year, month=last_month_date.month, day=1)
            next_invoice_end_date = date(year=last_month_date.year, month=last_month_date.month, day=date_range[1])
            cookies_to_set.append({
                'key': t,
                'value': date_encryption.encrypt(next_invoice_start_date, next_invoice_end_date)
            })
        else:
            is_current_month = last_invoice.month == current_month and last_invoice.year == current_year
            # Check if last invoice is still pending.
            if last_invoice.status in active_status:
                can_create = False
                next_invoice_start_date = None
                next_invoice_end_date = None
                message = 'Não é possível criar um novo recibo dado que o recibo anterior ainda está em processamento.'
                cookies_to_set.append({
                    'key': t,
                    'value': ''
                })
            # Check if previous invoice is rejected.
            elif last_invoice.status == 'rejected':
                can_create = True
                next_invoice_start_date = last_invoice.start_date
                next_invoice_end_date = last_invoice.end_date
                cookies_to_set.append({
                    'key': t,
                    'value': date_encryption.encrypt(next_invoice_start_date, next_invoice_end_date)
                })
            # Check if last invoice is from last month. (Current didn't end yet)
            elif last_invoice.start_date <= current_date - relativedelta(months=1) <= last_invoice.end_date:
                can_create = False
                next_invoice_start_date = None
                next_invoice_end_date = None
                message = 'Não é possível criar um novo recibo uma vez que o mês ainda não terminou.'
                cookies_to_set.append({
                    'key': t,
                    'value': ''
                })
            # Default action.
            else:
                next_invoice_date = last_invoice.start_date + relativedelta(months=1)
                date_range = calendar.monthrange(next_invoice_date.year, next_invoice_date.month)

                can_create = True
                next_invoice_start_date = date(year=next_invoice_date.year, month=next_invoice_date.month, day=1)
                next_invoice_end_date = date(year=next_invoice_date.year, month=next_invoice_date.month, day=date_range[1])
                cookies_to_set.append({
                    'key': t,
                    'value': date_encryption.encrypt(next_invoice_start_date, next_invoice_end_date)
                })

        # Add the next invoice data to the list.
        next_invoices[t] = {
            'can_create': can_create,
            'start_date': next_invoice_start_date.strftime('%d/%m/%Y') if next_invoice_start_date else None,
            'end_date': next_invoice_end_date.strftime('%d/%m/%Y') if next_invoice_end_date else None,
            'message': message
        }

    return next_invoices, cookies_to_set
