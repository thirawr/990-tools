from django.apps import apps
from core.models import *
from efile_export.models import Report


def get_return_type_label(return_type_code):
    return_type_map = {
        '1': ['990', '990O', '990EO'],
        '2': ['990EZ'],
        '3': ['990PF']
    }

    return_type_code = str(return_type_code)
    return return_type_map[return_type_code]


def get_fields_from_sked_part(parent_sked_part_id):
    # fields_qs = Field_Metadata.objects.filter(
    #     parent_sked_part_id=parent_sked_part_id
    # )

    fields_qs = Schedule_Part_Metadata.objects.get(id=parent_sked_part_id).field_metadata_set.all()

    # take a field off the top
    sample_field = fields_qs[0]

    sked_part_key = sample_field.db_table
    sked_part_key = sked_part_key.replace('_', '')
    xpath = sample_field.xpath.lower()
    print(sked_part_key)
    if 'schedule' in xpath:
        sked_part_key_prefix = 'return'
    elif 'irs990pf' in xpath:
        sked_part_key_prefix = 'returnpf'
    elif 'irs990ez' in xpath:
        sked_part_key_prefix = 'returnez'
    else:
        sked_part_key_prefix = 'return'
    # if '990' in return_type_list:
    #     sked_part_key_prefix = 'return'  # idt this will work because we have multi-form schedules  - schedules always get return_ prefix
    # elif '990EZ' in return_type_list:
    #     sked_part_key_prefix = 'returnez'
    # else:
    #     sked_part_key_prefix = 'returnpf'
    sked_part_key = sked_part_key_prefix + sked_part_key  # this should be the db table name now
    print(sked_part_key)

    return sked_part_key, fields_qs


    # fields = []
    #
    # for field in fields_qs:
    #     sked_part_key = field.db_table
    #     sked_part_key = sked_part_key.replace('_', '')
    #     xpath = field.xpath.lower()
    #     print(sked_part_key)
    #     if 'schedule' in xpath:
    #         sked_part_key_prefix = 'return'
    #     elif 'irs990pf' in xpath:
    #         sked_part_key_prefix = 'returnpf'
    #     elif 'irs990ez' in xpath:
    #         sked_part_key_prefix = 'returnez'
    #     else:
    #         sked_part_key_prefix = 'return'
    #     # if '990' in return_type_list:
    #     #     sked_part_key_prefix = 'return'  # idt this will work because we have multi-form schedules  - schedules always get return_ prefix
    #     # elif '990EZ' in return_type_list:
    #     #     sked_part_key_prefix = 'returnez'
    #     # else:
    #     #     sked_part_key_prefix = 'returnpf'
    #     sked_part_key = sked_part_key_prefix + sked_part_key  # this should be the db table name now
    #     print(sked_part_key)
    #     fields.append(field.attribute_name)


def get_object_ids(eins, fiscal_years):
    fy_object_id_map = {}

    for fy in fiscal_year:
        for ein in eins:
            try:
                org = FilingFiling.objects.get(tax_period__startswith=fy, ein=ein)
                object_id = org.object_id
                if fy not in fy_object_id_map.keys():
                    fy_object_id_map[fy] = [object_id]
                else:
                    fy_object_id_map[fy].append(object_id)

            except FilingFiling.DoesNotExist:
                continue  # nothing here

    return fy_object_id_map


def generate_report(request):
    # generate report obj here
    # @TODO: add report fields to form

    print(request.session.keys())
    # print(request.session['year'])
    sked_part_ids = request.session.get('schedule_parts', None)
    if not sked_part_ids:
        pass  # raise something here

    sked_part_field_map = {}

    return_type_list = get_return_type_label(request.session.get('return_type', None))

    # prep the fieldlist
    for sked_part_id in sked_part_ids:
        sked_part_key, fields_qs = get_fields_from_sked_part(sked_part_id)
        sked_part_field_map[sked_part_key] = fields_qs

    print(sked_part_field_map)

    # prep the fy: objcet_id map
    yrs = request.session.get('year', None)
    eins = request.session.get('eins', None)
    if not yrs or not eins:
        pass   # raise something
    fy_object_id_map = get_object_ids(yrs, eins)
