# coding: utf-8

import os
import glob

__product__ = 'Python'
__version__ = '0.4'

from clocwalk.libs.core.common import recursive_search_files


def _get_version(version_str):
    """
    get version
    :param version_str:
    :return:
    """

    name, version = version_str, ''
    ver_seps = ('==', '>=', '<=', "~=")

    for sep in ver_seps:
        if sep in version_str:
            name, version = version_str.split(sep)

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
                'vendor': '',
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
    # TODO setup.py

    code_dir = kwargs.get('code_dir', '')
    file_name = kwargs.get('file_name', 'requirements.txt')
    skipNewVerCheck = kwargs.get('skipNewVerCheck', False)

    result_file_list = recursive_search_files(code_dir, '*/requirements.txt')

    _ = glob.glob(os.path.join(code_dir, 'requirements', '*.txt'))
    if _:
        result_file_list.extend(_)

    result = []

    for item in result_file_list:
        # FIXME
        relative_path = item.replace('{0}'.format(code_dir), '')
        relative_path = relative_path[1:] if relative_path.startswith('/') else relative_path
        result.extend(_get_dependencies(file_name=item, origin=relative_path))

    return result
