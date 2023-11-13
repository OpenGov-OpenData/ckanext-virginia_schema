
# encoding: utf-8

from ckan.plugins import toolkit as tk
import ckan.lib.navl.dictization_functions as df
import datetime as dt


unflatten = df.unflatten
missing = tk.missing
StopOnError = tk.StopOnError
get_validator = tk.get_validator
_ = tk._
get_action = tk.get_action
h = tk.h


def timeframe_validator(keys, flattened_data, errors, context):

    data = unflatten(flattened_data)
    extras = flattened_data.get(('__extras',), {}) or None
    if extras:
        flattened_data.pop(('__extras',), None)

    date_from = data.get('start_date')
    date_to = data.get('end_date')


    if date_from and date_to:
        if date_from > date_to:
            errors[keys].append(_('Date from must be before date to'))
    elif date_from:
        errors[keys].append(_('Date to is required'))
    elif date_to:
        errors[keys].append(_('Date from is required'))
    
    # combine date_from and date_to into a single field
    if date_from and date_to:
        data_collection_timeframe = '{} - {}'.format(date_from, date_to)
        flattened_data[keys] = data_collection_timeframe

    
    
    