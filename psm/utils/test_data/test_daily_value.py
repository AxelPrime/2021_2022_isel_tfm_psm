from datetime import datetime

from financial.models import DailyValue


def create_test_daily_value():
    date_today = datetime.utcnow()

    DailyValue.objects.create(
        value=43,
        start_date=datetime(year=date_today.year, month=1, day=1),
        end_date=datetime(year=date_today.year, month=12, day=31)
    )
