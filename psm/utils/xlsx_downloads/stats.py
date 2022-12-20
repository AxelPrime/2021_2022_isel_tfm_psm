from datetime import datetime

import xlsxwriter
from django.core.files.temp import NamedTemporaryFile

from entities.models import CareHouse
from financial.models import TypologyStats

MONTH_COLS = {
    "1": {
        "name": "Janeiro",
        "cols": ["C", "D", "E"],
    },
    "2": {
        "name": "Fevereiro",
        "cols": ["F", "G", "H"],
    },
    "3": {
        "name": "Março",
        "cols": ["I", "J", "K"],
    },
    "4": {
        "name": "Abril",
        "cols": ["L", "M", "N"],
    },
    "5": {
        "name": "Maio",
        "cols": ["O", "P", "Q"],
    },
    "6": {
        "name": "Junho",
        "cols": ["R", "S", "T"],
    },
    "7": {
        "name": "Julho",
        "cols": ["U", "V", "W"],
    },
    "8": {
        "name": "Agosto",
        "cols": ["X", "Y", "Z"],
    },
    "9": {
        "name": "Setembro",
        "cols": ["AA", "AB", "AC"],
    },
    "10": {
        "name": "Outubro",
        "cols": ["AD", "AE", "AF"],
    },
    "11": {
        "name": "Novembro",
        "cols": ["AG", "AH", "AI"],
    },
    "12": {
        "name": "Dezembro",
        "cols": ["AJ", "AK", "AL"],
    }
}


class StatsDownload:
    """
    Class used to provide the files relating to the care house and typology stats.

    Attributes
    ----------
    stats: TypologyStats
        the stats object.

    temp_file: NamedTemporaryFile
        the temp filewhere the data will be written.
    """

    def __init__(self, stats: TypologyStats):
        self.stats = stats
        self.temp_file = NamedTemporaryFile(suffix=".xlsx")

    def __create_file(self, data):
        """
        Function used to insert the doanload data in the temp file.

        Parameters
        ----------
        data: dict
            the data to add to the file

        """

        # Obtain the total number of care houses.
        care_house_count = CareHouse.objects.all().count()
        # Create the workbook.
        workbook = xlsxwriter.Workbook(filename=self.temp_file.name)
        # Add a worksheet to the book.
        worksheet = workbook.add_worksheet()

        # Add the static data to the file.
        worksheet.merge_range("A1:A2", "Tipologia")
        worksheet.merge_range("B1:B2", "Unidades Prestadoras")

        # Iterate the month data.
        for k, v in MONTH_COLS.items():
            # Add the month headers.
            worksheet.merge_range(f"{v['cols'][0]}1:{v['cols'][-1]}1", v["name"])
            worksheet.write(f"{v['cols'][0]}2", "Nº Pacientes")
            worksheet.write(f"{v['cols'][1]}2", "Diárias")
            worksheet.write(f"{v['cols'][2]}2", "Diárias (€)")

        # Set the current writting row.
        current_row = 3

        # Iterate the file data.
        for tip, tip_data in data.items():
            # Check if there is a need to merge cells.
            if care_house_count > 1:
                worksheet.merge_range(f"A{current_row}:A{current_row + care_house_count - 1}", tip)
            else:
                worksheet.write(f"A{current_row}", tip)

            # Iterate the care house data.
            for care_house_id, care_house_data in tip_data.items():
                # Add the date house name to the file.
                care_house_name = care_house_data['name']
                worksheet.write(f"B{current_row}", care_house_name)
                # Iterate the monthly data.
                for month_number, month_data in care_house_data['months'].items():
                    # Write the month dta in the colomns.
                    worksheet.write(f"{MONTH_COLS[month_number]['cols'][0]}{current_row}", month_data["total_patients"])
                    worksheet.write(f"{MONTH_COLS[month_number]['cols'][1]}{current_row}", month_data["total_dailies"])
                    worksheet.write(f"{MONTH_COLS[month_number]['cols'][2]}{current_row}", month_data["total_amount"])
                # Increment the current row.
                current_row += 1
        # Close and save the file.
        workbook.close()

    def create_typology_stats_file(self):
        """
        Function used to create the typology stats file

        Returns
        -------
        file, filename: tuple[NamedTemporaryFile, str]
            a tuple object containing the temp file with the data and the name of the download file.
        """

        # Create the name for the file.
        filename = f"Estatisticas_Tipologia_2022_{datetime.utcnow().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
        # Create insert the data in the file.
        self.__create_file(self.stats.typology_stats)
        # Return the file and respective name.
        return self.temp_file, filename

    def create_care_house_stats_file(self):
        """
        Function used to create the care house stats file

        Returns
        -------
        file, filename: tuple[NamedTemporaryFile, str]
            a tuple object containing the temp file with the data and the name of the download file.
        """

        # Create the name for the file.
        filename = f"Estatisticas_Casas_Saude_2022_{datetime.utcnow().strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"
        # Create insert the data in the file.
        self.__create_file(self.stats.care_house_stats)
        # Return the file and respective name.
        return self.temp_file, filename
