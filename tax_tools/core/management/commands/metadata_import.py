from django.core.management.base import BaseCommand, CommandError
from core.models import Field_Metadata, Schedule_Part_Metadata

'''
kk so i dont think it's really all that necessary to \update\ these tables
the metadata tables are somewhat static, so we should delete the old rows and
replace them with the new on "update"
'''


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pass
