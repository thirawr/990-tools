from django.core.management.base import BaseCommand, CommandError
from core.models import Organization
# '''
# kk so i dont think it's really all that necessary to \update\ these tables
# the metadata tables are somewhat static, so we should delete the old rows and
# replace them with the new on "update"
# '''


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sql = '''
            CREATE VIEW core_organization AS (
                select
                    ein,
                    taxpayer_name
                FROM
                    990s.filing_filing
                WHERE id in (
                    SELECT
                        MAX(id)
                    FROM 990s.filing_filing
                    GROUP BY ein
                )
            );
        '''

        Organization.objects.raw('DROP TABLE core_organization;')
        Organization.objects.raw(sql)
