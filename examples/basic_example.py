from HclObject import HclObject

hcl_obj = HclObject(is_root=True)
hcl_obj.add_attribute(type='locals', values=[
    HclObject(attribute_name='cpu_util_server_pod', type='dict_equal', values=[
            HclObject(attribute_name='title', type='str', values='"CPU Usage Per server Pod (%)"'),
            HclObject(attribute_name='viz', type='str', values='"timeseries"'),
            HclObject(attribute_name='autoscale', type='boolean', values='true'),
            HclObject(attribute_name='request', type='list', values=[
                    HclObject(type='dict_raw', values=[
                        HclObject(attribute_name='q', type='str', values='"max:kubernetes.memory.working_set'),
                        HclObject(attribute_name='type', type='str', values='"line"'),
                    ])
                ]
            ),
        ]
    )]
)

result = hcl_obj.generate_hcl()
print(result)


""" Result is like below.
locals {
  cpu_util_server_pod = {
    title = "CPU Usage Per server Pod (%)"
    viz = "timeseries"
    autoscale = true
    request = [
      {
        q = "max:kubernetes.memory.working_set
        type = "line"
      }
    ]
  }
}
"""
