from datetime import timedelta, date, datetime
from financial.models import YearlyInvoice

import xlsxwriter


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def run():
    receipt = YearlyInvoice.objects.get(year=2022)

    filename = f"Recibo_2022_{datetime.utcnow().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"

    workbook = xlsxwriter.Workbook(filename=filename)
    worksheet = workbook.add_worksheet()

    header_cols = [
        "Nome do Paciente",
        "Mês",
        "Inicio Contabilização",
        "Fim Contabilização",
        "Diárias",
        "Diárias (€)",
    ]

    header_format = workbook.add_format({
        'bold': True,
    })

    for col_num, data in enumerate(header_cols):
        worksheet.write(0, col_num, data, header_format)

    for row_num, line in enumerate(receipt.data['lines']):
        for col, data in enumerate(line):
            if col == len(line) - 1:
                continue
            worksheet.write(row_num + 1, col, data)

    workbook.close()
