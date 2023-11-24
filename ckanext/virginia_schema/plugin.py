import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


import ckanext.virginia_schema.helpers as helpers
import ckanext.virginia_schema.validators as validators

class VirginiaSchemaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets','virginia_schema')

#         config_['scheming.presets'] = """
# ckanext.scheming:presets.json
# """

#         config_['scheming.dataset_schemas'] = """
# ckanext.virginia_schema:virginia_dataset.yaml
# """

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_json_element': helpers.get_json_element,
        }
    
    # IValidators
    def get_validators(self):
        return {
            'timeframe_validator': validators.timeframe_validator,
        }
