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
        CREATE TABLE core_organization AS
          (SELECT `990s`.`filing_filing`.`id` AS `id`,
                  `990s`.`filing_filing`.`ein` AS `ein`,
                  `990s`.`filing_filing`.`taxpayer_name` AS `taxpayer_name`
           FROM `990s`.`filing_filing`
           WHERE `990s`.`filing_filing`.`id` IN
               (SELECT max(`990s`.`filing_filing`.`id`)
                FROM `990s`.`filing_filing`
                GROUP BY `990s`.`filing_filing`.`ein`))
        '''

        Organization.objects.raw('DROP TABLE core_organization;')
        Organization.objects.raw(sql)
