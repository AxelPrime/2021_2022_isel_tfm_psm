from datetime import date
from typing import List

from django.db.models import QuerySet

from financial.models import DailyValue
from internment_management.models import CareHouseInternment, ActivityLog
from functools import reduce

DATE_FORMAT = "%Y-%m-%d"


class InvoiceCreation:
    """
    Class used to create the monthly invoice data.
    """
    def __init__(
            self,
            dates_list: List[date],
            internment_list: QuerySet[CareHouseInternment],
            daily_values: QuerySet[DailyValue]
    ):
        """
        Initialization method.

        Parameters
        ----------
        dates_list: list
            the complete list of dates for the invoice.

        internment_list: QuerySet
            the list of internments.

        daily_values: QuerySet
            the list of values to be applied in the invoice.
        """
        self.dates_list = dates_list
        self.internment_list = internment_list
        self.daily_values = daily_values

    def __find_interned_dates(self, activity_logs: QuerySet[ActivityLog]):
        """
        Private method used to find the effective days the patient was interned.

        Parameters
        ----------
        activity_logs: QuerySet
            the list of activity logs of the internment.

        Returns
        -------
        dates_list: list
            returns the list of dates the patient was effectively interned.
        """

        # Create a copy of the list of dates.
        dates_list_copy = self.dates_list.copy()
        # Iterate the given activity logs.
        for i in range(activity_logs.count()):
            # Obtain the Activity Log of the current index.
            al = activity_logs[i]

            # Check if the activity log type is an Entrance.
            if al.activity_type == 'entry':
                # Remove the dates that are older than the current log date.
                dates_list_copy[:] = [d for d in dates_list_copy if d >= al.log_date.date()]
            # Check if the log type is a temporary Leave (e.g. External Consultation).
            elif al.activity_type == 'temporary_leave':
                # Check if the current log is the last log.
                if i + 1 == activity_logs.count() or activity_logs[i + 1].activity_type != 'return':
                    # Remove the dates that are newer than the current log.
                    dates_list_copy[:] = [d for d in dates_list_copy if d <= al.log_date.date()]
                else:
                    # Remove the dates between the current log and next log.
                    dates_list_copy[:] = [
                        d
                        for d in dates_list_copy if al.log_date.date() >= d or d >= activity_logs[i + 1].log_date.date()
                    ]
            # Check if the current log type is a Return.
            elif al.activity_type == 'return':
                # Check if the current log is the oldest.
                if i - 1 < 0:
                    # Remove the dates that are older than the current log.
                    dates_list_copy[:] = [d for d in dates_list_copy if d >= al.log_date.date()]
                else:
                    # Remove tge dates between the current log and the previous log.
                    dates_list_copy[:] = [
                        d
                        for d in dates_list_copy if
                        activity_logs[i - 1].log_date.date() >= d or d >= al.log_date.date()]
            # Action for a Exit log.
            else:
                # Remove the dates that are newer than the current log.
                dates_list_copy[:] = [d for d in dates_list_copy if d <= al.log_date.date()]

        # Return the filtered list.
        return dates_list_copy

    def __get_values_applied(self, dates_interned: List[date]):
        """
        Private method used to obtain the values applied in the internment.

        Parameters
        ----------
        dates_interned: list
            the list of activity logs of the internment.

        Returns
        -------
        values_applied: list
            returns a list containing the values to apply.
        """

        # List to return.
        values_applied = []
        # The last day of the invoice.
        invoice_end_date = self.dates_list[-1]
        # Iterate the list of daily values.
        for i in range(self.daily_values.count()):
            # Obtain the daily value in the current index.
            v = self.daily_values[i]
            # Obtain the true end date of the valu to apply.
            end_date = v.end_date if v.end_date else invoice_end_date
            # Check if the current value is the first value.
            if i - 1 < 0:
                # Obtain the days that are older than the current end date.
                days = [d for d in dates_interned if d <= end_date]
            else:
                # Obtain the previous value end date.
                v_1_date = self.daily_values[i - 1].end_date
                # Obtain the days between the previous value end date and the true end date.
                days = [d for d in dates_interned if v_1_date < d <= end_date]
            # Append the data to the final list.
            values_applied.append({
                'value': v.value,
                'days': len(days)
            })
        # Return the list of values to apply in to this internment.
        return values_applied

    def get_invoice_data(self):
        """
        Method used to obtain the invoice data..

        Returns
        -------
        invoice_data: dict
            returns a list containing the invoice data for each patient interned in the care house.
        """

        # The final invoice data list.
        invoice_data = []
        # Iterate the internments.
        for ip in self.internment_list:  # type: CareHouseInternment
            # Obtain the activity logs.
            activity_logs = ip.activitylog_set.filter(
                log_date__range=(self.dates_list[0], self.dates_list[-1])
            ).order_by('log_date')
            # Get the interned dates.
            dates_interned = self.__find_interned_dates(activity_logs)
            # Get the values to apply.
            values_applied = self.__get_values_applied(dates_interned)
            # Add the data to the final list.
            invoice_data.append({
                'patient_name': ip.referral.patient.name,
                'referral_id': ip.referral.identifier,
                'internment_id': ip.identifier,
                'invoice_start': dates_interned[0].strftime(DATE_FORMAT),
                'invoice_end': dates_interned[-1].strftime(DATE_FORMAT),
                'total_days': len(dates_interned),
                'total_amount': reduce(
                    lambda x, y: x + (y['value'] * y['days']),
                    values_applied,
                    0
                ),
                "values_applied": values_applied
            })
        # Return the data list.
        return {
            'data': invoice_data
        }
