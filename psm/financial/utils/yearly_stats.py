from entities.models import CareHouse
from ..models import TypologyStats, MonthlyInvoice
from functools import reduce

MONTHS = {
    '1': 'Janeiro',
    '2': 'Fevereiro',
    '3': 'Março',
    '4': 'Abril',
    '5': 'Maio',
    '6': 'Junho',
    '7': 'Julho',
    '8': 'Agosto',
    '9': 'Setembro',
    '10': 'Outubro',
    '11': 'Novembro',
    '12': 'Dezembro',
}


def update_typology_stats(invoice: MonthlyInvoice):
    """
    Function used to create or update the yearly typology stats.
    
    Parameters
    ----------
    invoice: MonthlyInvoice
        the monthly invoice with the data to add to the stats.
    """

    # Obtain the typology stats for the year or create it.
    try:
        stats = TypologyStats.objects.get(year=invoice.year)
    except TypologyStats.DoesNotExist:
        stats = TypologyStats(
            year=invoice.year,
            care_house_stats={"todo": "todo"}
        )
        care_house_list = [
            {
                "name": c.name,
                "identification_code": c.identification_code
            }
            for c in CareHouse.objects.all()
        ]
        stats_data = {
            "I": {},
            "II": {},
            "III": {}
        }
        for k, v in stats_data.items():
            for c in care_house_list:
                care_house_obj = {
                    'name': c['name'],
                    'months': {}
                }
                for number, name in MONTHS.items():
                    care_house_obj['months'][str(number)] = {
                        "total_amount": "-",
                        "total_patients": "-",
                        "total_dailies": "-"
                    }
                stats_data[k].update({
                    c['identification_code']: care_house_obj
                })

        care_house_data = {
            "I + II + III": {},
            "I + III": {},
        }
        for k, v in care_house_data.items():
            for c in care_house_list:
                care_house_obj = {
                    'name': c['name'],
                    'months': {}
                }
                for number, name in MONTHS.items():
                    care_house_obj['months'][str(number)] = {
                        "total_amount": "-",
                        "total_patients": "-",
                        "total_dailies": "-"
                    }
                care_house_data[k].update({
                    c['identification_code']: care_house_obj
                })

        stats.typology_stats = stats_data
        stats.care_house_stats = care_house_data
        stats.save()

    # Get the invoice data.
    invoice_data = invoice.invoice_lines

    # Add the data to the stats.
    stats.typology_stats[invoice.typology][invoice.care_house.identification_code]['months'][str(invoice.month)] = {
        "total_amount": invoice_data['total_amount'],
        "total_patients": invoice_data['total_patients'],
        "total_dailies": reduce(lambda a, b: a + b['total_days'], invoice_data['data'], 0),
    }

    tip_i_data = stats.typology_stats['I'][invoice.care_house.identification_code]['months'][str(invoice.month)]
    tip_ii_data = stats.typology_stats['II'][invoice.care_house.identification_code]['months'][str(invoice.month)]
    tip_iii_data = stats.typology_stats['III'][invoice.care_house.identification_code]['months'][str(invoice.month)]

    if invoice.typology != 'II':
        stats.care_house_stats['I + III'][invoice.care_house.identification_code]['months'][str(invoice.month)] = {
            "total_amount": float(0 if tip_i_data['total_amount'] == '-' else tip_i_data['total_amount'])
                            + float(0 if tip_iii_data['total_amount'] == '-' else tip_iii_data['total_amount']),
            "total_patients": float(0 if tip_i_data['total_patients'] == '-' else tip_i_data['total_patients'])
                            + float(0 if tip_iii_data['total_patients'] == '-' else tip_iii_data['total_patients']),
            "total_dailies": float(0 if tip_i_data['total_dailies'] == '-' else tip_i_data['total_dailies'])
                            + float(0 if tip_iii_data['total_dailies'] == '-' else tip_iii_data['total_dailies']),
        }

    stats.care_house_stats['I + II + III'][invoice.care_house.identification_code]['months'][str(invoice.month)] = {
        "total_amount": float(0 if tip_i_data['total_amount'] == '-' else tip_i_data['total_amount'])
        + float(0 if tip_iii_data['total_amount'] == '-' else tip_iii_data['total_amount'])
        + float(0 if tip_ii_data['total_amount'] == '-' else tip_ii_data['total_amount']),
        "total_patients": float(0 if tip_i_data['total_patients'] == '-' else tip_i_data['total_patients'])
        + float(0 if tip_iii_data['total_patients'] == '-' else tip_iii_data['total_patients'])
        + float(0 if tip_ii_data['total_patients'] == '-' else tip_ii_data['total_patients']),
        "total_dailies": float(0 if tip_i_data['total_dailies'] == '-' else tip_i_data['total_dailies'])
        + float(0 if tip_iii_data['total_dailies'] == '-' else tip_iii_data['total_dailies'])
        + float(0 if tip_ii_data['total_dailies'] == '-' else tip_ii_data['total_dailies']),
    }

    stats.save()
