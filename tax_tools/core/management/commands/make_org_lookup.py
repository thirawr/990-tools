from django.core.management.base import BaseCommand, CommandError
from core.models import Organization, FilingFiling, Fiscal_Year
from django.db import transaction

# '''
# kk so i dont think it's really all that necessary to \update\ these tables
# the metadata tables are somewhat static, so we should delete the old rows and
# replace them with the new on "update"
# '''


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # filings = FilingFiling.objects.all().order_by('-id')
        # num_filings = filings.count()
        # print('Beginning import of {0} filings from 990 database'.format(num_filings))

        # for idx, filing in enumerate(filings):
        #     pct_processed = ((idx + 1)/ float(num_filings)) * 100
        #     print('Processing filing {0} of {1} ({2}%)'.format(idx + 1, num_filings, pct_processed))
        #     ein = filing.ein
        #     taxpayer_name = filing.taxpayer_name
        #     return_type = filing.return_type
        #     tax_period = filing.tax_period
        #     fiscal_year = int(str(tax_period)[:4])
        #     org, created = Organization.objects.get_or_create(ein=ein)
        #
        #     if created:
        #         #  save only the most recent values
        #         org.taxpayer_name = taxpayer_name
        #         org.return_type = return_type
        #         org.save()
        #
        #     fiscal_year, created = Fiscal_Year.objects.get_or_create(fiscal_year=fiscal_year, organization=org)
        #
        #     if created:
        #         fiscal_year.save()
        #     else:
        #         pass  # not sure lol

        orgs_sql = '''
        INSERT INTO `core_organization` (`ein`, `taxpayer_name`, `return_type`)
          (SELECT `990s`.`filing_filing`.`ein` AS `ein`,
                  `990s`.`filing_filing`.`taxpayer_name` AS `taxpayer_name`,
                  `990s`.`filing_filing`.`return_type` AS `return_type`
           FROM `990s`.`filing_filing`
           WHERE `990s`.`filing_filing`.`id` IN
               (SELECT max(`990s`.`filing_filing`.`id`)
                FROM `990s`.`filing_filing`
                GROUP BY `990s`.`filing_filing`.`ein`));
        '''

        Organization.objects.raw('DELETE FROM core_organization;')
        Organization.objects.raw(orgs_sql)
        print('Orgs added')

        orgs = Organization.objects.all()
        num_orgs = orgs.count()

        FY_BATCH_LIMIT = 5000
        fy_batch_num = 1
        fy_batch = []

        Fiscal_Year.objects.all().delete()

        for idx, org in enumerate(orgs):
            pct_completed = ((idx + 1) / float(num_orgs)) * 100
            print('Processing org {0} out of {1} ({2}%)...'.format(idx+1, num_orgs, pct_completed))
            filings = FilingFiling.objects.filter(ein=org.ein)
            fy_added = []
            for filing in filings:
                fiscal_year = int(str(filing.tax_period)[:4])
                if fiscal_year not in fy_added:
                    fy_added.append(fiscal_year)
                    fy = Fiscal_Year(fiscal_year=fiscal_year, organization=org)
                    fy_batch.append(fy)
                if len(fy_batch) >= FY_BATCH_LIMIT:
                    print('Committing batch #{0}...'.format(fy_batch_num))
                    Fiscal_Year.objects.bulk_create(fy_batch)
                    fy_batch = []
                    fy_batch_num += 1


        # fy_sql = '''
        #
        # '''
