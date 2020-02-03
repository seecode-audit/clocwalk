# coding: utf-8

import re
from xml.etree import ElementTree

from clocwalk.libs.core.common import recursive_search_files
from clocwalk.libs.core.common import strip
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import logger

__product__ = 'Java'
__version__ = '0.3'

NAMESPACES = {
    'xmlns': 'http://maven.apache.org/POM/4.0.0'
}


class PomEntity(object):

    def __init__(self, pom_content, origin_file_name='', parent_file=''):
        """

        :param origin_file_name:
        :param pom_content:
        """
        # property
        self._group_id = ''
        self._artifact_id = ''
        self._version = ''
        self._file_name = origin_file_name
        self._parent_file = parent_file
        self._parent = {}
        self._key = ''
        self._properties = {}
        self._dependencies = []
        self._sub_dependencies = []
        self.doc = ElementTree.fromstring(pom_content)

        artifact_id = self.doc.find("./xmlns:artifactId", namespaces=NAMESPACES)
        version = self.doc.find("./xmlns:version", namespaces=NAMESPACES)
        group_id = self.doc.find("./xmlns:groupId", namespaces=NAMESPACES)

        self._group_id = group_id.text if group_id is not None else None
        self._artifact_id = artifact_id.text if artifact_id is not None else None
        self._version = version.text if version is not None else None

        # group_id is None use parent
        if self.parent and not self._group_id and self.parent['groupId']:
            self._group_id = self.parent['groupId']

    @property
    def group_id(self):
        return self._group_id

    @property
    def artifact_id(self):
        return self._artifact_id

    @property
    def file_name(self):
        return self._file_name

    @property
    def parent_file(self):
        return self._parent_file

    @property
    def version(self):
        return self._version

    @property
    def parent(self):
        """

        :return:
        """
        if not self._parent:
            parent_node = self.doc.find(".//xmlns:parent", namespaces=NAMESPACES)
            if parent_node is not None:
                for item in parent_node:
                    name = re.sub(r'^\{.+?\}', '', item.tag)
                    self._parent[name] = item.text
        return self._parent

    @property
    def key(self):
        """

        :return:
        """
        return '{0}:{1}'.format(self.group_id, self.artifact_id)

    @property
    def properties(self):
        """

        :return:
        """
        if not self._properties:
            prop_list = self.doc.find(".//xmlns:properties", namespaces=NAMESPACES)

            if prop_list is not None:
                for item in prop_list:
                    name = re.sub(r'^\{.+?\}', '', item.tag)
                    value = item.text if item is not None else ''
                    self._properties[name] = value

                # ${xx.vresion}
                for k, v in self._properties.items():
                    if v:
                        name = re.search(r'^\$\{(.+?)\}', v)
                        if name and name.group(1) in self._properties:
                            self._properties[k] = self._properties[name.group(1)]
        return self._properties

    @property
    def dependencies(self):
        if not self._dependencies:
            deps = self.doc.findall(".//xmlns:dependencies", namespaces=NAMESPACES)

            if deps is not None:
                for item in deps:
                    for dependency in item.getchildren():
                        try:
                            artifact_id = dependency.find("xmlns:artifactId", namespaces=NAMESPACES)
                            version = dependency.find("xmlns:version", namespaces=NAMESPACES)
                            group_id = dependency.find("xmlns:groupId", namespaces=NAMESPACES)
                            real_ver = ''

                            if version is not None and version.text:
                                ver = re.search(r'\$\{(.+?)\}', strip(version.text), re.I)
                                if ver and ver.group(1) in self.properties:
                                    real_ver = self.properties[ver.group(1)]
                                else:
                                    real_ver = strip(version.text)
                            self._dependencies.append({
                                'artifact_id': artifact_id.text,
                                'version': real_ver,
                                'group_id': re.sub(r'^\{.+?\}', '', group_id.text),
                            })
                        except Exception as ex:
                            import traceback;
                            traceback.print_exc()
                            logger.warn(ex)

        return self._dependencies


def recursive_online(url, parent_file=None, deep_recursive=False):
    """

    :param url:
    :param parent_file:
    :param deep_recursive:
    :return:
    """
    result = []
    html = kb.http_cache.get(url)
    if html:
        pom = PomEntity(parent_file=parent_file, pom_content=html, origin_file_name=url)
        result.append(pom)

        # parent
        if pom.parent and pom.parent['version'] and '${' not in pom.parent['version']:
            _url = '{0}{1}/{2}/{3}/{2}-{3}.pom'.format(
                conf.mvn['repo'][0],
                pom.parent['groupId'].replace('.', '/'),
                pom.parent['artifactId'],
                pom.parent['version'],
            )
            result.extend(recursive_online(_url, parent_file=parent_file, deep_recursive=deep_recursive))

        # fix ${xxx.version}
        if pom.dependencies and pom.key in kb.dependencies:
            for dep in pom.dependencies:
                ver = re.search(r'\$\{(.+?)\}', strip(dep['version']), re.I)
                if ver and ver.group(1) in kb.dependencies[pom.key].properties:
                    dep['version'] = kb.dependencies[pom.key].properties[ver.group(1)]

        # all
        if deep_recursive and pom.dependencies:
            for item in pom.dependencies:
                if item['version'] and '${' not in item['version']:
                    _url = '{0}{1}/{2}/{3}/{2}-{3}.pom'.format(
                        conf.mvn['repo'][0],
                        item['group_id'].replace('.', '/'),
                        item['artifact_id'],
                        item['version'],
                    )
                    result.extend(recursive_online(_url, parent_file=parent_file, deep_recursive=deep_recursive))

    return result


def start(**kwargs):
    """
    :param kwargs:
    :return:
    """
    code_dir = kwargs.get('code_dir', '')
    enable_online_recursive = kwargs.get('enable_online_recursive', False)
    deep_recursive = kwargs.get('deep_recursive', False)
    pom_file_list = recursive_search_files(code_dir, '*/pom.xml')

    pom_entity_list = []
    result = []

    for item in pom_file_list:
        logger.info('[-] Start analysis "{0}" file...'.format(item))
        with open(item, 'rb') as fp:
            pom_content = fp.read()
            pom = PomEntity(origin_file_name=item, pom_content=pom_content.decode())
            if not pom.parent:
                if pom.key not in kb.dependencies:
                    kb.dependencies[pom.key] = pom
            pom_entity_list.append(pom)

    if enable_online_recursive:
        _result = []
        for pom in pom_entity_list:
            for dep in pom.dependencies:
                if dep['version']:
                    _url = '{0}{1}/{2}/{3}/{2}-{3}.pom'.format(
                        conf.mvn['repo'][0],
                        dep['group_id'].replace('.', '/'),
                        dep['artifact_id'],
                        dep['version'],
                    )
                    _result.extend(recursive_online(url=_url, parent_file=pom.file_name, deep_recursive=deep_recursive))
        pom_entity_list.extend(_result)

    for pom in pom_entity_list:
        parent_key = None
        parent_file = ''
        if pom.parent:
            parent_key = '{0}:{1}'.format(pom.parent['groupId'], pom.parent['artifactId'])
            if parent_key and parent_key in kb.dependencies:
                parent_file = kb.dependencies[parent_key].file_name

        for item in pom.dependencies:
            version = item['version']
            ver = re.search(r'\$\{(.+?)\}', version, re.I)
            if ver and parent_key and parent_key in kb.dependencies and ver.group(1) in kb.dependencies[parent_key].properties:
                version = kb.dependencies[parent_key].properties[ver.group(1)]

            result.append({
                'vendor': item['group_id'],
                'product': item['artifact_id'],
                'version': version,
                'new_version': '',
                'cve': {},
                'parent_file': parent_file if parent_file else pom.parent_file,
                'origin_file': pom.file_name,
            })

    return result
