# from fund_accounting_app.models import
import fund_accounting_app.operations.book_interest as default
from django.core.management.base import BaseCommand, CommandError
import datetime


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise CommandError(msg)


class Command(BaseCommand):

    help = "Add new fund manager and book the cash."

    def handle(self, *args, **options):

        default.book_interest_all_deals_from_last_booking_day()

        self.stdout.write(
            self.style.SUCCESS("Successfully added fund manager and booked cash")
        )
