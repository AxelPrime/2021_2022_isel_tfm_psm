from datetime import datetime

import xlsxwriter
from django.core.files.temp import NamedTemporaryFile

from financial.models import TypologyIIMonthlyStats


class TypologyIIStatsDownload:
    """
    Class used to download the Typology II Stats file.
    """

    def __init__(self, stats: TypologyIIMonthlyStats):
        self.stats = stats
        self.temp_file = NamedTemporaryFile(suffix=".xlsx")

    def create_file(self):
        """
        Function used to create the file to download.

        Returns
        -------
        file, filename : tuple
            the created file and respective name.
        """

        # Create the file name.
        filename = f"Tip_II_{self.stats.get_month_display()}_{self.stats.year}_{datetime.utcnow().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"

        # Create the Workbook with the temp file.
        workbook = xlsxwriter.Workbook(filename=self.temp_file.name)
        # Add a worksheet to the book.
        worksheet = workbook.add_worksheet()

        # Define the columns of the header.
        header_cols = [
            "Nome da Instituição",
            "NIF",
            "Código",
            "Total de Pacientes",
            "Diárias (€)",
        ]
        # Define the format for the header.
        header_format = workbook.add_format({
            'bold': True,
        })

        # Add the header to the sheet.
        for col_num, data in enumerate(header_cols):
            worksheet.write(0, col_num, data, header_format)

        # Set the current row to write.
        current_row = 1
        # Iterate the data and add to the file.
        for institution_code, data in self.stats.data['institutions'].items():
            worksheet.write(current_row, 0, data['name'])
            worksheet.write(current_row, 1, data['nif'])
            worksheet.write(current_row, 2, institution_code)
            worksheet.write(current_row, 3, data['data']["total_patients"])
            worksheet.write(current_row, 4, data['data']["amount"])

            # Increment the current row.
            current_row += 1
        # Save and close the book.
        workbook.close()

        return self.temp_file, filename
