import os
from datetime import datetime

import xlsxwriter
from django.core.files.temp import NamedTemporaryFile

from financial.models import YearlyInvoice


class YearlyInvoiceDownload:
    """
    Class used to create a yearly invoice XLSX file for donwload.

    Attributes
    ----------
    invoice: YearlyInvoice
        the invoice to create the file for.

    """
    def __init__(self, invoice: YearlyInvoice, temp_file: NamedTemporaryFile):
        self.temp_file = temp_file
        self.invoice = invoice
        self.filename = f"Recibo_{self.invoice.year}_{datetime.utcnow().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"

    def create_invoice_xlsx(self):
        """
        Method used to create the temp file.

        Returns
        -------
        filename: str
            the path to the file created.
        """
        # Open a work book.
        workbook = xlsxwriter.Workbook(filename=self.temp_file.name)
        # Add the worksheet to work on.
        worksheet = workbook.add_worksheet()

        # Define the columns of the header.
        header_cols = [
            "Nome do Paciente",
            "Mês",
            "Inicio Contabilização",
            "Fim Contabilização",
            "Diárias",
            "Diárias (€)",
        ]
        # Define the format for the header.
        header_format = workbook.add_format({
            'bold': True,
        })

        # Add the header to the sheet.
        for col_num, data in enumerate(header_cols):
            worksheet.write(0, col_num, data, header_format)

        # Iterate the invoice lines and add to the file.
        for row_num, line in enumerate(self.invoice.data['lines']):
            for col, data in enumerate(line):
                if col == len(line) - 1:
                    continue
                worksheet.write(row_num + 1, col, data)

        # Save and close the workbook.
        workbook.close()

        # Return the name of the file.
        return self.filename

    def delete_invoice_file(self):
        """
        Delete the temp file.
        """
        os.remove(self.filename)
