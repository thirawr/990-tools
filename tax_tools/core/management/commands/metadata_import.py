from django.core.management.base import BaseCommand, CommandError
from core.models import Field_Metadata, Schedule_Part_Metadata, Schedule_Metadata
from tax_tools.settings import XML_METADATA_DIR
from ast import literal_eval
import csv
import os

# '''
# kk so i dont think it's really all that necessary to \update\ these tables
# the metadata tables are somewhat static, so we should delete the old rows and
# replace them with the new on "update"
# '''


class Command(BaseCommand):
    def read_csv(self, path):
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    def handle(self, *args, **kwargs):
        variables_path = os.path.join(XML_METADATA_DIR, 'variables.csv')
        variables_rows = self.read_csv(variables_path)

        schedule_parts_path = os.path.join(XML_METADATA_DIR, 'schedule_parts.csv')
        schedule_parts_rows = self.read_csv(schedule_parts_path)

        Field_Metadata.objects.all().delete()
        Schedule_Part_Metadata.objects.all().delete()

        for row in schedule_parts_rows:
            parent_sked_name = row['parent_sked']
            try:
                parent_sked = Schedule_Metadata.objects.get(name=parent_sked_name)
            except Schedule_Metadata.DoesNotExist:
                parent_sked = Schedule_Metadata(name=parent_sked_name)
                parent_sked.save()
            part_key = row['parent_sked_part']
            ordering = row['ordering']
            part_name = row['part_name']
            xml_root = row['xml_root']
            is_shell = literal_eval(row['is_shell'].title())

            print('Processing sked part {xml_root}'.format(xml_root=xml_root))

            sked_part = Schedule_Part_Metadata(
                parent_sked=parent_sked,
                part_key=part_key,
                ordering=ordering,
                part_name=part_name,
                xml_root=xml_root,
                is_shell=is_shell
            )

            sked_part.save()


        for row in variables_rows:
            parent_sked_name = row['parent_sked']
            parent_sked = Schedule_Metadata.objects.get(name=parent_sked_name)
            parent_sked_part_key = row['parent_sked_part']
            parent_sked_part = Schedule_Part_Metadata.objects.get(part_key=parent_sked_part_key)
            ordering = row['ordering']
            in_a_group = literal_eval(row['in_a_group'].title())
            db_table = row['db_table']
            db_name = row['db_name']
            xpath = row['xpath']
            irs_type = row['irs_type']
            db_type = row['db_type']
            line_number = row['line_number']
            description = row['description']
            versions = row['versions']

            attribute_name = db_name.lower()

            print('Processing field {xpath}'.format(xpath=xpath))

            field = Field_Metadata(
                parent_sked=parent_sked,
                parent_sked_part=parent_sked_part,
                ordering=ordering,
                in_a_group=in_a_group,
                db_table=db_table,
                db_name=db_name,
                attribute_name=attribute_name,
                xpath=xpath,
                irs_type=irs_type,
                db_type=db_type,
                line_number=line_number,
                description=description,
                versions=versions
            )

            field.save()


        print('done!')
