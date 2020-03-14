import json
from HclObject import HclObject

with open('value_names.json') as json_file:
    value_names = json.load(json_file)

with open('dashboard.json') as json_file:
    dashboard_data = json.load(json_file)

with open('var.json') as json_file:
    var_json = json.load(json_file)

hcl_obj = HclObject(is_root=True)
data = []

for widget in dashboard_data['widgets']:
    for panel in widget['definition']['widgets']:
        if panel['definition']['type'] == 'timeseries':
            requests = []
            for q in panel["definition"]["requests"]:
                requests.append(HclObject(type='dict_raw', values=[
                    HclObject(attribute_name='q', type='str', values=f'"{q["q"]}"'),
                    HclObject(attribute_name='type', type='str',
                              values=f'"{q["display_type"]}"'),
                ]))

            data.append(HclObject(attribute_name=f'{value_names[len(data)]}', type='dict_equal', values=[
                HclObject(attribute_name='title', type='str', values=f'"{panel["definition"]["title"]}"'),
                HclObject(attribute_name='viz', type='str', values='"timeseries"'),
                HclObject(attribute_name='autoscale', type='boolean', values='true'),
                HclObject(attribute_name='request', type='list', values=
                    requests
                ),
            ]))
        else: #timeseries가 아닌 경우
            pass

hcl_obj.add_attribute(type='locals', values=data)
result = hcl_obj.generate_hcl()

for key, val in var_json.items():
    result = result.replace(val, f'${{var.{key}}}')

print(result)

