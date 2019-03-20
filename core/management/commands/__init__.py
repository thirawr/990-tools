from django.core.management.base import BaseCommand, CommandError
from core.models import Field_Metadata, Schedule_Part_Metadata


VARIABLES_CSV_PATH = ''
SCHEDULE_PARTS_CSV_PATH = ''


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        pass
