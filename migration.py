# encoding: utf-8
import argparse
import codecs
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
from ckan import model
import csv

import logging

log = logging.getLogger(__name__)

_context = None

def get_context():
    global _context
    if not _context:
        user = logic.get_action(u'get_site_user')(
            {u'model': model, u'ignore_auth': True}, {})
        _context = {u'model': model, u'session': model.Session,
                    u'user': user[u'name'],
                    u'auth_user_obj': user,
                    u'return_id_only': True,
                    u"ignore_auth": True}
    return _context


def load_datasets():
    context = get_context()
    search_data_dict = {
        u"q": u"",
        u"rows": 1000,
        u"include_private": True
    }

    return toolkit.get_action('package_search')(context, search_data_dict)["results"]

def convert_extras(dataset, i):
    # count datasets and print
    print(f"Dataset {i}: {dataset['name']}")
    # get extras
    if not dataset['extras']:
        return
    extras = dataset.pop('extras', None) 
    for extra in extras:
        
        # convert extras to dict
        if extra['key'] == 'collection_frequency' or 'collection_frequency' in extra['key'] :
            dataset['data_collection_frequency'] = extra['value']
        
        if extra['key'] == 'collection_procedures' or 'collection_procedures' in extra['key'] :
            dataset['data_collection_procedures'] = extra['value']

        if extra['key'] == 'collection_timeframe' or 'collection_timeframe' in extra['key']:
            dataset['data_collection_timeframe'] = extra['value']
        
        if extra['key'] == 'coordinate_system' or 'coordinate_system' in extra['key']:
            dataset['coordinate_reference_system'] = extra['value']

        if extra['key'] == 'data_uses' or 'known_uses_of_data' in extra['key']:
            dataset['known_uses_of_data'] = extra['value']

        if extra['key'] == 'license_id' or extra['key'] == 'license_id':
            dataset['license_id'] = extra['value']

        if extra['key'] == 'publish_frequency' or 'publishing_frequency' in extra['key']:
            dataset['data_publishing_frequency'] = extra['value']

        if extra['key'] == 'publish_method' or extra['key'] == 'data_publishing_method':
            dataset['data_publishing_frequency'] = extra['value']

        if extra['key'] == 'quality_procedures' or extra['key'] == 'data_quality_procedures':
            dataset['data_quality_procedures'] = extra['value']

        if extra['key'] == 'subdivision' or extra['key'] == 'data_subdivision':    
            dataset['subdivision'] = extra['value']
    
    resources = dataset['resources']
    res_copy = resources.copy()
    for resource in res_copy:
        for key in resource:
            if key == 'collection_frequency' or key == 'data_collection_frequency' :
                dataset['data_collection_frequency'] = resource[key]
                resource.pop('collection_frequency', None)
            if key == 'collection_procedures' or key == 'data_collection_procedures':
                dataset['data_collection_procedures'] = resource[key]
                resource.pop('collection_procedures', None)
            if key == 'collection_timeframe' or key == 'data_collection_timeframe':
                dataset['data_collection_timeframe'] = resource[key]
                resource.pop('collection_timeframe', None)
            if key == 'coordinate_system' or key == 'coordinate_reference_system':
                dataset['coordinate_reference_system'] = resource[key]
                resource.pop('coordinate_system', None)
            if key == 'data_uses' or key == 'known_uses_of_data':
                dataset['known_uses_of_data'] = resource[key]
                resource.pop('data_uses', None)
            if key == 'publish_frequency' or key == 'data_publishing_frequency':
                dataset['data_publishing_frequency'] = resource[key]
                resource.pop('publish_frequency', None)
            if key == 'publish_method' or key == 'data_publishing_method':
                dataset['data_publishing_method'] = resource[key]
                resource.pop('publish_method', None)
            if key == 'quality_procedures' or key == 'data_quality_procedures':
                dataset['data_quality_procedures'] = resource[key]
                resource.pop('quality_procedures', None)
            if  key == 'resource_division' or key == 'data_subdivision':
                dataset['subdivision'] = resource[key]
                resource.pop(key, None)
            if key =='resource_division' or key == 'resource_division':
                dataset['division'] = resource[key]
                resource.pop(key, None)
            if  key == 'resource_contact_name':
                dataset['contact_name'] = resource[key]
                resource.pop(key, None)
            if  key == 'resource_contact_email':
                dataset['contact_email'] = resource[key]
                resource.pop(key, None)
            if  key == 'resource_contact_phone':
                dataset['contact_phone'] = resource[key]
                resource.pop(key, None)

        update_resource(resource)


    update_dataset(dataset)



def update_dataset(dataset):
    context = get_context()
    res = toolkit.get_action('package_update')(context, dataset)
    if res:
        print("success")

def update_resource(resource):
    context = get_context()
    res = toolkit.get_action('resource_update')(context, resource)
    if res:
        print("res success")


def migrate_extras():
    # Collect the datasets with `package_search`
    # and include private datasets W
    context = get_context()
    datasets = load_datasets()
    success = []
    errors = []
    data = {}
    i = 1
    print(f"Total datasets: {len(datasets)}")
    for dataset in datasets:
        try:
           convert_extras(dataset,i)
           i += 1
        except Exception as e:
            print(e)

if __name__ == u'__main__':
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument(u'-c', u'--config', help=u'CKAN config file (.ini)')
    args = parser.parse_args()
    assert args.config, u'You must supply a --config'
    print(u'Loading config')
    try:
        from ckan.cli import load_config
        from ckan.config.middleware import make_app
        make_app(load_config(args.config))
    except Exception as e:
        print(e)
    migrate_extras()