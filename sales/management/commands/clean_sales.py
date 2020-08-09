# Denne management cmd skal benyttes til å mappe VMÅ->Untappd
from django.core.management.base import BaseCommand
from sales.models import DailySale
from datetime import date,datetime,timedelta

class Command(BaseCommand):
    help = '''
    Clean up old sales data and keep data for the last 7 days.
    '''

    def handle(self, *args, **options):
        # Log when the job is executed
        self.stdout.write(f"Cleaning up Daily Sales Data @ {datetime.now()}")

        # Number of days to keep sales data for. Older sales data will be cleaned (deleted)
        DAYS_TO_KEEP = 7

        old_sales = DailySale.objects.filter(sales_day__lte = date.today() - timedelta(DAYS_TO_KEEP) )
        deleted_data = old_sales.delete()

        # -(-1) is due to <= in Queryset above, keeping the last 7 days including today
        self.stdout.write(f"Keeping sales data from: {date.today() - timedelta(DAYS_TO_KEEP - 1)}")
        self.stdout.write(f"Deleted the following data: {deleted_data}")


        return