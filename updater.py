import argparse
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

def clean_string(input_string):
    return input_string.replace('\0', '')

def update_dataset(row):
    context = get_context()
    
    # get dataset
    dataset = toolkit.get_action('package_show')(context, {'id': row['ï»¿identifier']})
    
    extras = dataset.pop('extras', None)
    print(dataset.get('name'))
    dataset['contact_name'] = row['contact_name']
    dataset['contact_email'] = row['contact_email']
    dataset['contact_phone'] = row['contact_phone']

    # update dataset
    toolkit.get_action('package_update')(context, dataset)
    
    # print dataset
    print(dataset)
    

def read_csv():
    with open('nm-csv1.csv', mode='r', encoding='latin1') as csv_file:
        lines = [clean_string(line) for line in csv_file]
    
    # Create a CSV reader object
    csv_reader = csv.DictReader(lines)
    
    # Iterate over each row as a dictionary
    for row in csv_reader:
        update_dataset(row)
        

def main():
    context = get_context()
    csv_data = read_csv()


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
    main()