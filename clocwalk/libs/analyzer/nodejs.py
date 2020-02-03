# coding: utf-8

import json

__product__ = 'JavaScript'
__version__ = '0.3'

from clocwalk.libs.core.common import recursive_search_files


def _get_dependencies(file_name='package.json', origin=None):
    """
    get properties
    :param file_name:
    :return:
    """
    result = []
    with open(file_name, 'r') as fp:
        json_obj = json.load(fp)
        for tag in ['dependencies', 'devDependencies']:
            for name, ver in json_obj[tag].items():
                result.append({
                    'vendor': tag,
                    'product': name,
                    'version': ver,
                    'new_version': '',
                    'parent_file': '',
                    'cve': {},
                    'origin_file': file_name,
                })
    return result


def start(**kwargs):
    """
    :param kwargs:
    :return:
    """
    code_dir = kwargs.get('code_dir', '')
    file_name = kwargs.get('file_name', 'package.json')
    skipNewVerCheck = kwargs.get('skipNewVerCheck', False)
    result_file_list = recursive_search_files(code_dir, '*/package.json')

    result = []

    for item in result_file_list:
        # FIXME
        relative_path = item.replace('{0}'.format(code_dir), '')
        relative_path = relative_path[1:] if relative_path.startswith('/') else relative_path

        result.extend(_get_dependencies(file_name=item, origin=relative_path))

    return result
