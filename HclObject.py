class HclObject():
    attribute_name = []

    def __init__(self, attribute_name=None, type=None, values=None, is_root=False):
        self.is_root = is_root
        if not is_root:
            self.attribute_name = attribute_name
            self.type = type
            self.values = values

    def add_attribute(self, type='', resource_name=None, name=None, values=None):
        self.attribute_name.append({
            'type': type,
            'resource_name': resource_name,
            'name': name,
            'values': values
        })

    def generate_hcl(self):
        data = ''
        result = ''
        for node in self.attribute_name:
            if node['type'] == 'locals':
                data += f'locals {{\n'
            else:
                data += f'{node["type"]} "{node["resource_name"]}" "{node["name"]}" {{\n'
            for item in node['values']:
                result += self.traverse_nodes(item, 0)
            data += f'{result}}}\n\n'
        return data

    def traverse_nodes(self, node, depth):
        depth += 1
        margin = (depth * 2) * ' '
        result = ''

        if node.type == 'dict':
            result += f'{margin}{node.attribute_name} {{\n'
            for item in node.values:
                if item.type == 'str' or item.type == 'boolean':
                    result += f'  {margin}{item.attribute_name} = ' + (f'{item.values}\n' if item.type == 'str' else f'{item.values}\n')
                else:
                    result += f'{self.traverse_nodes(item, depth)}'
            result += f'{margin}}}\n'

        elif node.type == 'dict_equal':
            result += f'{margin}{node.attribute_name} = {{\n'
            for item in node.values:
                if item.type == 'str' or item.type == 'boolean':
                    result += f'  {margin}{item.attribute_name} = ' + (f'{item.values}\n' if item.type == 'str' else f'{item.values}\n')
                else:
                    result += f'{self.traverse_nodes(item, depth)}'
            result += f'{margin}}}\n'

        elif node.type == 'list':
            result += f'{margin}{node.attribute_name} = [\n'
            lst = []
            for item in node.values:
                if item.type == 'str' or item.type == 'boolean':
                    lst.append((f'  {margin}{item.values}' if item.type == 'str' else f'{item.values}'))
                else:
                    lst.append(f'{self.traverse_nodes(item, depth)}'[0:-1])
            result += ', \n'.join(lst) + f'\n{margin}]\n'

        elif node.type == 'list_raw':
            result += f'{margin}[{", ".join(node.values)}]\n'

        elif node.type == 'dict_raw':
            result += f'{margin}{{\n'
            for item in node.values:
                if item.type == 'str' or item.type == 'boolean':
                    result += f'  {margin}{item.attribute_name} = ' + (f'{item.values}\n' if item.type == 'str' else f'{item.values}\n')
                else:
                    result += f'{self.traverse_nodes(item, depth)}'
            result += f'{margin}}}\n'
        return result

