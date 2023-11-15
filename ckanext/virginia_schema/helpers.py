import json


def get_json_element(data, subfield, field=None):
    if not data:
        return ''
    json_data = json.loads(data)
    if field:
        try:
            field_name = field.get('field_name')
        except AttributeError:
            field_name = field
        return json_data.get(subfield.get('field_name')).get(field_name)
    return json_data.get(subfield)


def is_data_dict_active(ddict):
    """"Returns True if data dictionary is populated"""
    for col in ddict:
        info = col.get('info', {})
        if info.get('label') or info.get('notes'):
            return True
    return False
