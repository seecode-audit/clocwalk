# coding: utf-8

import os
import re

from clocwalk.libs.core.common import recursive_search_files
from clocwalk.libs.core.data import logger

__product__ = 'Java'
__version__ = '0.1'

"""
https://docs.gradle.org/current/dsl/org.gradle.api.Project.html#N14F2A
https://docs.gradle.org/current/javadoc/org/gradle/api/Project.html#files-java.lang.Object...-
"""


def find_include_file(content):
    """
    https://docs.gradle.org/current/dsl/org.gradle.api.Project.html#org.gradle.api.Project:rootProject
    :param content:
    :return:
    """
    result = None
    kw = re.compile(r'rootProject\.file\("(.+)?"\)')
    conf_content = ''
    if isinstance(content, list):
        conf_content = '\n'.join(content)
    elif isinstance(content, str):
        conf_content = content

    find_list = kw.findall(conf_content)

    if find_list:
        result = [_ for _ in list(set(find_list)) if _.endswith('.gradle')]  # FIXME .gradle other?

    return result


def find_keyword_block(content, keyword='dependencies', l_bracket='{', r_bracket='}'):
    """

    :param content:
    :param keyword:
    :param l_bracket:
    :param r_bracket:
    :return:
    """
    kw = re.compile(' {0} '.format(keyword), re.I)
    result = {}
    left_brackets = 0
    right_brackets = 0
    line_number = 0
    current_dep_num = None
    if isinstance(content, str):
        content_list = content.split('\n')
    elif isinstance(content, list):
        content_list = content
    else:
        # FIXME raise Exception?
        content_list = None

    if content_list:
        is_found_keyword = False
        for item in content_list:
            line_number += 1
            if kw.search(item):
                current_dep_num = line_number
                result[str(current_dep_num)] = []
                is_found_keyword = True
                left_brackets += item.count(l_bracket)
                right_brackets += item.count(r_bracket)
                continue

            if is_found_keyword:
                if item.strip() and item.strip() not in (r_bracket,):
                    result[str(current_dep_num)].append(item)
                left_brackets += item.count(l_bracket)
                right_brackets += item.count(r_bracket)

            if left_brackets == right_brackets:
                current_dep_num, is_found_keyword = None, False

    return result


def find_version_info(content, keyword, name):
    """

    :param content:
    :param keyword:
    :param name:
    :return:
    """
    result = ''
    version_list = find_keyword_block(content, keyword, l_bracket='[', r_bracket=']')

    if version_list:
        for _, item in version_list.items():
            for line in item:
                if ':' in line:
                    current_line = line.strip()
                    n, v = current_line.split(':')
                    if name == n.strip():
                        result = v.strip().replace('"', '').replace("'", "").replace(',', '')
                        return result

    return result


def find_product_info(content, origin_file=None):
    """

    :param content:
    :param origin_file:
    :return:
    """
    conf_content = content
    if isinstance(content, str):
        conf_content = conf_content.split('\n')

    result = []
    version = {}

    for item in conf_content:
        current_line = item.strip()
        # full name
        #  compile group: 'org.apache.struts', name: 'struts2-core', version: '2.5.5'
        if ' group ' in item and ' name ' in item and ' version ' in item:
            line = current_line[current_line.index(" ") + 1:]
            product = {
                'new_version': '', 'cve': '', 'parent_file': '', 'origin_file': origin_file
            }
            for b in line.split(","):
                if ":" in b:
                    key, value = b.split(":")
                    if 'group' in key:
                        key = 'vendor'
                    elif 'name' in key:
                        key = 'product'
                    elif 'version' in key:
                        v_r = re.search(r'\$\{*(\w+?)\.(\w+)?\}*', value)
                        if v_r:
                            section, name = v_r.group(1), v_r.group(2)
                            value = find_version_info(content, section, name)
                    product[key] = value
            if product:
                result.append(product)
        else:  # fast
            info_re = re.search(r"[\"']{1}(.+?)[\"']{1}", current_line)
            if info_re:
                info = info_re.group(1).split(':')
                if len(info) == 2:
                    result.append({
                        'vendor': info[0],
                        'name': info[1],
                        'version': '',
                        'new_version': '',
                        'cve': '',
                        'parent_file': '',
                        'origin_file': origin_file,
                    })
                elif len(info) == 3:
                    value = info[2]
                    v_r = re.search(r'\$\{*(\w+?)\.(\w+)?\}*', info[2])
                    if v_r:
                        section, name = v_r.group(1), v_r.group(2)
                        value = find_version_info(content, section, name)
                    result.append({
                        'vendor': info[0],
                        'name': info[1],
                        'version': value,
                        'new_version': '',
                        'cve': '',
                        'parent_file': '',
                        'origin_file': origin_file,
                    })
    return result


def start(**kwargs):
    """
    :param kwargs:
    :return:
    """
    code_dir = kwargs.get('code_dir', '')
    file_list = recursive_search_files(code_dir, '*/build.gradle')
    result = []

    for item in file_list:
        origin_file = item[len(code_dir) + 1:]
        logger.info('[-] Start analysis "{0}" file...'.format(origin_file))
        with open(item, 'rb') as fp:
            content = fp.read().decode()
            include_file = find_include_file(content)
            if include_file:
                path, _ = os.path.split(item)
                for f in include_file:
                    full_path = os.path.join(path, f)
                    with open(full_path, 'rb') as fpi:
                        result.extend(find_product_info(fpi.read().decode(), full_path[len(code_dir) + 1:]))

            dependencies = find_keyword_block(content)
            for key, value in dependencies.items():
                result.extend(find_product_info(value, origin_file))

    return result
