# coding: utf-8

import os
import json
import glob

__product__ = 'JavaScript'
__version__ = '0.2'


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
            for name, ver in json_obj[tag].iteritems():
                result.append({
                    'name': name,
                    'version':  ver,
                    'tag':  tag,
                    'origin': origin,
                    'new_version': ''
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

    result_file_list = glob.glob(os.path.join(code_dir, file_name)) + \
        glob.glob(os.path.join(code_dir, '*', file_name)) + \
        glob.glob(os.path.join(code_dir, '*', '*', file_name)) + \
        glob.glob(os.path.join(code_dir, '*', '*', '*', file_name))

    result = []

    for item in result_file_list:
        # FIXME
        relative_path = item.replace('{0}/'.format(code_dir), '')
        result.extend(_get_dependencies(file_name=item, origin=relative_path))

    return result
