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
    fields_qs = Field_Metadata.objects.filter(
        parent_sked_part_id=parent_sked_part_id
    )

    for field in fields_qs:
        sked_part_key = field.db_table
        sked_part_key = sked_part_key.replace('_', '')
        if '990' in return_type_list:
            sked_part_key_prefix = 'return'
        elif '990EZ' in return_type_list:
            sked_part_key_prefix = 'returnez'
        else:
            sked_part_key_prefix = 'returnpf'
        sked_part_key = sked_part_key_prefix + sked_part_key  # this should be the db table name now
        if sked_part_key not in sked_part_field_map.keys():
            sked_part_field_map[sked_part_key] = [field.attribute_name]
        else:
            sked_part_field_map[sked_part_key].append(field.attribute_name)




def generate_report(request):
    # generate report obj here
    # @TODO: add report fields to form

    print(request.session.keys())
    sked_part_ids = request.session.get('schedule_parts', None)
    if not sked_part_ids:
        pass  # raise something here

    sked_part_field_map = {}

    return_type_list = get_return_type_label(request.session.get('return_type', None))

    for sked_part_id in sked_part_ids:
        fields_qs = get_fields_from_sked_part(sked_part_id)
