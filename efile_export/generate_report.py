from django.apps import apps
from core.models import *
from efile_export.models import Report

import zipfile
import io
import csv

from itertools import chain
from datetime import datetime
from ast import literal_eval


def get_return_type_label(return_type_code):
    return_type_map = {
        '1': ['990', '990O', '990EO'],
        '2': ['990EZ'],
        '3': ['990PF']
    }

    return_type_code = str(return_type_code)
    return return_type_map[return_type_code]


def get_fields_metadata_from_sked_part(parent_sked_part_id):
    # fields_qs = Field_Metadata.objects.filter(
    #     parent_sked_part_id=parent_sked_part_id
    # )
    # address edge cases herE?

    fields_qs = Schedule_Part_Metadata.objects.get(id=parent_sked_part_id).field_metadata_set.all()

    # take a field off the top
    # sample_field = fields_qs[0]

    db_table_fields_map = {}

    for field in fields_qs:

        db_table_name = field.db_table
        db_table_name = db_table_name.replace('_', '')
        xpath = field.xpath.lower()
        # print(sked_part_key)
        # if 'schedule' in xpath:
        #     db_table_name_prefix = 'return'
        # elif 'irs990pf' in xpath:
        #     db_table_name_prefix = 'returnpf'
        # elif 'irs990ez' in xpath:
        #     db_table_name_prefix = 'returnez'
        # else:
        db_table_name_prefix = 'return'
        # if '990' in return_type_list:
        #     sked_part_key_prefix = 'return'  # idt this will work because we have multi-form schedules  - schedules always get return_ prefix
        # elif '990EZ' in return_type_list:
        #     sked_part_key_prefix = 'returnez'
        # else:
        #     sked_part_key_prefix = 'returnpf'
        model_name = db_table_name_prefix + db_table_name  # this should be the db table name now
        # print(sked_part_key)

        if model_name not in db_table_fields_map.keys():
            db_table_fields_map[model_name] = [field]
        else:
            db_table_fields_map[model_name].append(field)

    return db_table_fields_map


def get_object_ids(eins, fiscal_years):
    fy_object_id_map = {}

    # print(fiscal_years)
    for fy in fiscal_years:
        # print(fy)
        # print(type(eins))
        for ein in eins:
            # print('ein:', ein)
            possible_filings = FilingFiling.objects.filter(tax_period__startswith=fy, ein=ein)
            # print('pf: ', possible_filings)
            if not possible_filings:
                continue  # nothing here, continue on
            elif len(possible_filings) > 1:
                # case for multiple return sin one tax period
                sorted_filings = sorted(possible_filings, key=lambda x: strptime(x.sub_date.split(' ')[0], '%m/%d/%Y'))
                most_recent_filing = sorted_filings[0]
            else:
                most_recent_filing = possible_filings[0]

                object_id = most_recent_filing.object_id
                if fy not in fy_object_id_map.keys():
                    fy_object_id_map[fy] = [object_id]
                else:
                    fy_object_id_map[fy].append(object_id)

    return fy_object_id_map


def get_db_table_row(object_id, sked_part_key):
    sked_part_model = apps.get_model('core', sked_part_key)
    try:
        rows = sked_part_model.objects.filter(object_id=object_id)
        # print('f:', rows)
    except sked_part_model.DoesNotExist:
        return None
    else:
        return rows


def generate_csv_files(model_name_rows_map, model_name_field_map):

    sked_part_file_map = {}

    files = {}

    # gotta pull values from db_table rather than sked_part_key
    # for sked_part_key, sked_fields in model_name_field_map.items():
    #     for object_id in object_ids:
    #         for field in sked_fields:
    #             att_name = field.attribute_name  # use this to key our final dict
    #             model_name = field.db_table  # i think we can use this to reference the correct table

    CONSTANT_FIELDS = ['id', 'ein', 'object_id']

    for model_name, rows in model_name_rows_map.items():
        mem_file = io.StringIO()
        fields_qs = model_name_field_map[model_name]
        field_names = [field.attribute_name for field in fields_qs]
        field_names = CONSTANT_FIELDS + field_names
        # with open(mem_file, 'w') as f:
        writer = csv.DictWriter(mem_file, fieldnames=field_names)
        writer.writeheader()
        # print(field_names)
        for row in rows:
            new_row = {}
            for field_name in field_names:
                # field_name = field.attribute_name
                if field_name not in new_row.keys():
                    # print(row)
                    new_row[field_name] = getattr(row, field_name)
            writer.writerow(new_row)

        if model_name not in files.keys():
            files[model_name] = mem_file

    return files


def get_eins_from_org_ids(org_ids):
    orgs = Organization.objects.filter(id__in=org_ids)
    return [org.ein for org in orgs]


def generate_report(request):
    # generate report obj here
    # @TODO: add report fields to form

    # print(request.session.keys())
    # print(request.session['year'])
    sked_part_ids = request.session.get('schedule_parts', None)
    if not sked_part_ids:
        pass  # raise something here

    model_name_field_meta_map = {}
    # hm i dont think we need the fields actually
    # just gotta pull * from the table
    # this may be useful for later tho

    return_type_list = get_return_type_label(request.session.get('return_type', None))

    # prep the fieldlist
    model_name_field_meta_map = {}
    for sked_part_id in sked_part_ids:
        model_name_field_meta_map_part = get_fields_metadata_from_sked_part(sked_part_id)
        model_name_field_meta_map.update(model_name_field_meta_map_part)
        # model_name_field_meta_map[db_table_name] = fields_qs

    # print(model_name_field_meta_map)

    # prep the fy: objcet_id map
    yrs = request.session.get('year', None)
    org_ids = literal_eval(request.session.get('org_id', None))
    # print(org_ids)
    # print(type(org_ids))
    if not yrs or not org_ids:
        pass   # raise something

    eins = get_eins_from_org_ids(org_ids)
    fy_object_id_map = get_object_ids(eins, yrs)
    # print('fy_object_id_map: ', fy_object_id_map)

    object_ids = []
    for object_id_list in fy_object_id_map.values():
        object_ids += object_id_list
    # print('object_ids: ', object_ids)

    model_name_rows_map = {}
    for db_table_name in model_name_field_meta_map.keys():
        # if db_table_name not in model_name_rows_map.keys():
            # model_name_rows_map[db_table_name] = []
        for object_id in object_ids:
            rows = get_db_table_row(object_id, db_table_name)
            if rows:
                for row in rows:
                    if db_table_name not in model_name_rows_map.keys():
                        model_name_rows_map[db_table_name] = [row]
                    else:
                        model_name_rows_map[db_table_name].append(row)

    # print(sked_part_rows_map)

    files = generate_csv_files(model_name_rows_map, model_name_field_meta_map)
    # print('files: ', files)

    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w') as f:
        for model_name, file in files.items():
            f.writestr('{model_name}.csv'.format(model_name=model_name), file.getvalue())

    archive.seek(0)

    return archive


    # make the csvs
    # zip the csvs
    # return the csvs for streaming



    # pull relevant fields from each objectid return

    #
