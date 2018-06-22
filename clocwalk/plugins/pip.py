# coding: utf-8

import os
import glob

__product__ = 'Python'
__version__ = '0.2'


def _get_version(version_str):
    """
    get version
    :param version_str:
    :return:
    """
    if '==' in version_str:
        name, version = version_str.split('==')
    elif '>=' in version_str:
        name, version = version_str.split('>=')
    elif '<=' in version_str:
        name, version = version_str.split('<=')
    else:
        name, version = version_str, ''

    return name, version


def _get_dependencies(file_name='requirements.txt', origin=None):
    """
    get dependencies
    :param file_name:
    :param origin:
    :return:
    """
    result = []

    with open(file_name, 'r') as fp:
        for line in fp:
            name, ver = _get_version(line.strip())
            result.append({
                'name': name,
                'version':  ver,
                'tag':  '',
                'origin': origin,
                'new_version': ''
            })

    return result


def start(**kwargs):
    """
    :param kwargs:
    :return:
    """
    # TODO setup.py

    code_dir = kwargs.get('code_dir', '')
    file_name = kwargs.get('file_name', 'requirements.txt')
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
