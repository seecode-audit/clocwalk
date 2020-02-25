#!/usr/bin/env python
# coding: utf-8

import datetime
import glob
import gzip
import json
import os
import shutil
import time
import re

import gevent
import requests
from gevent.threadpool import ThreadPool

from clocwalk.libs.core.data import logger
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import paths
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.db_helper import DBHelper
from clocwalk.libs.detector.cvecpe import cpe_parse
from clocwalk.libs.core.exception import NoUpgradeRequiredError


class Upgrade(object):

    def __init__(self, proxies=None, upgrade_interval='7d', http_timeout=15):
        """

        :param proxies:
        :param upgrade_interval:
        :param http_timeout:
        """
        self.http_timeout = int(http_timeout)
        self.cve_path = paths.CVE_PATH
        self.cve_cpe_db = paths.DB_FILE
        self.cpe_file = os.path.join(self.cve_path, 'nvdcpematch-1.0.json')
        interval_type = re.search(r'(\d+)(\w)', upgrade_interval)
        if interval_type and interval_type.group(2) in ('d', 'h'):
            if interval_type.group(2) == 'd':
                self.upgrade_interval = 60 * 60 * 24 * int(interval_type.group(1))
            elif interval_type.group(2) == 'h':
                self.upgrade_interval = 60 * 60 * int(interval_type.group(1))
            else:
                self.upgrade_interval = 60 * 60 * 24 * 7
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en;q=0.9",
            "connection": "keep-alive",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108"
        }
        self.headers.update(conf['http']['headers'])

        self.pool = ThreadPool(10)
        logger.debug('Proxies: {0}'.format(proxies))
        self.proxies = proxies

    def download_cpe_match_file(self):
        """

        :return:
        """
        try:
            url = 'https://nvd.nist.gov/feeds/json/cpematch/1.0/nvdcpematch-1.0.json.gz'
            logger.info('[DOWNLOAD] {0}'.format(url))
            with requests.get(
                url,
                headers=self.headers,
                stream=True,
                proxies=self.proxies,
                timeout=self.http_timeout,
                verify=False
            ) as r:
                r.raise_for_status()
                with open('{0}.gz'.format(self.cpe_file), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            logger.info("Start extracting '{0}' files...".format(self.cve_path))
            with gzip.open('{0}.gz'.format(self.cpe_file), 'rb') as f_in:
                with open(self.cpe_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.unlink('{0}.gz'.format(self.cpe_file))
        except Exception as ex:
            raise ex

    def download_cve_file(self):
        """

        :return:
        """

        def download_file(year):
            try:
                cve_file = os.path.join(self.cve_path, 'nvdcve-1.1-{0}.json.gz'.format(year))
                url = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{0}.json.gz'.format(year)
                logger.info('[DOWNLOAD] {0}'.format(url))
                with requests.get(
                    url,
                    headers=self.headers,
                    stream=True,
                    proxies=self.proxies,
                    timeout=self.http_timeout,
                    verify=False
                ) as r:
                    r.raise_for_status()
                    with open(cve_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                logger.info("Start extracting '{0}' files...".format(cve_file))
                with gzip.open(cve_file, 'rb') as f_in:
                    with open(os.path.join(self.cve_path, 'nvdcve-1.1-{0}.json'.format(year)), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.unlink(cve_file)
            except Exception as ex:
                raise ex

        current_year = datetime.datetime.now().year
        for i in range(2002, current_year + 1):
            self.pool.spawn(download_file, i)
        gevent.wait()

    def cve_upgrade(self):
        """
        :return:
        """
        def get_problem_type(info):
            """

            :return:
            """
            result = ''
            if 'problemtype_data' in info and info['problemtype_data']:
                if 'description' in info['problemtype_data'][0] and info['problemtype_data'][0]['description']:
                    result = info['problemtype_data'][0]['description'][0]['value']
            return result

        def get_links(info):
            """

            :return:
            """
            result = []
            if 'reference_data' in info and info['reference_data']:
                for ref in info['reference_data']:
                    result.append(ref['url'])
            return '\n'.join(result)

        kb.db = DBHelper(self.cve_cpe_db, is_create=True)
        kb.db.create_cve_table()

        json_path = '{0}/nvdcve-1.1*.json'.format(self.cve_path)
        json_list = glob.glob(json_path)
        cve_list = []
        for cve_file in json_list:
            with open(cve_file, 'rb') as fp:
                json_obj = json.load(fp)
                for _ in json_obj['CVE_Items']:
                    if not _['configurations']['nodes']:
                        continue

                    cve = _['cve']['CVE_data_meta']['ID']
                    problemtype = get_problem_type(_['cve']['problemtype'])
                    year_re = re.search(r'CVE-(\d+)-\d+', cve, re.I)
                    year = year_re.group(1)
                    links = get_links(_['cve']['references'])
                    description = _['cve']['description']['description_data'][0]['value']
                    if 'cpe_match' not in _['configurations']['nodes'][0]:
                        if 'children' in _['configurations']['nodes'][0]:
                            if 'cpe_match' in _['configurations']['nodes'][0]['children'][0]:
                                cpe_match = _['configurations']['nodes'][0]['children'][0]['cpe_match']
                    else:
                        cpe_match = _['configurations']['nodes'][0]['cpe_match']

                    for item in cpe_match:
                        """
                        cve, description, links, cvss_v2_severity,  cvss_v2_impactscore, cvss_v3_impactscore
                        """
                        v3 = _['impact']['baseMetricV3']['impactScore'] if 'baseMetricV3' in _['impact'] else ''

                        cve_list.append((
                            cve,
                            item['cpe23Uri'],
                            description,
                            links,
                            problemtype,
                            year,
                            _['impact']['baseMetricV2']['severity'],
                            _['impact']['baseMetricV2']['impactScore'],
                            v3,
                        ))
                        if len(cve_list) % 1000000 == 0:
                            kb.db.create_cve_bulk(cve_list)
                            cve_list = []

        if cve_list:
            kb.db.create_cve_bulk(cve_list)

    @property
    def last_update_time(self):
        return datetime.datetime.fromtimestamp(int(os.stat(self.cve_cpe_db).st_atime))

    @property
    def is_update(self):
        result = False
        if os.path.isfile(self.cve_cpe_db):
            stat = os.stat(self.cve_cpe_db)
            if int(time.time()) - int(stat.st_mtime) > self.upgrade_interval:
                result = True
        else:
            result = True

        if conf.force_update:
            result = True

        if result:
            try:
                if os.path.isdir(self.cve_path):
                    shutil.rmtree(self.cve_path)
                os.makedirs(self.cve_path)
                if os.path.isdir(paths.CACHE_PATH):
                    shutil.rmtree(paths.CACHE_PATH)
                os.makedirs(paths.CACHE_PATH)
                if os.path.isfile(self.cve_cpe_db):
                    shutil.move(self.cve_cpe_db, '{0}.bak'.format(self.cve_cpe_db))
            except Exception as ex:
                logger.warn(ex)

        return result

    def cpe_upgrade(self):
        """

        :return:
        """
        kb.db = DBHelper(self.cve_cpe_db, is_create=True)
        kb.db.create_cpe_table()
        with open(self.cpe_file, 'rb') as fp:
            json_obj = json.load(fp)
            obj_list = []
            for cpes in json_obj['matches']:
                cpe23_uri = cpes['cpe23Uri']
                version_start_including = cpes['versionStartIncluding'] if 'versionStartIncluding' in cpes else ''
                version_end_including = cpes['versionEndIncluding'] if 'versionEndIncluding' in cpes else ''
                version_start_excluding = cpes['versionStartExcluding'] if 'versionStartExcluding' in cpes else ''
                version_end_excluding = cpes['versionEndExcluding'] if 'versionEndExcluding' in cpes else ''

                for item in cpes['cpe_name']:
                    cpe_part = cpe_parse(item['cpe23Uri'])
                    obj_list.append((
                        cpe_part["vendor"],
                        cpe_part["product"],
                        cpe_part["version"],
                        cpe_part["update"],
                        cpe23_uri,
                        cpe_part["edition"],
                        cpe_part["language"],
                        cpe_part["sw_edition"],
                        cpe_part["target_sw"],
                        cpe_part["target_hw"],
                        cpe_part["other"],
                        version_start_including,
                        version_end_including,
                        version_start_excluding,
                        version_end_excluding,
                    ))
                if len(obj_list) % 100000 == 0:
                    kb.db.create_cpe_bulk(obj_list)
                    obj_list = []
            if obj_list:
                kb.db.create_cpe_bulk(obj_list)

    def start(self):
        try:
            s_time = time.time()
            if self.is_update:
                self.download_cpe_match_file()
                self.download_cve_file()
                logger.info('File download is complete and data synchronization begins...')
                self.cpe_upgrade()
                self.cve_upgrade()
                logger.info('Rule upgrade succeeded.')
            else:
                raise NoUpgradeRequiredError("No upgrade required, last update time: {0}.".format(
                    self.last_update_time))
            logger.info('Total time consumption: {0}(s)'.format(round(time.time() - s_time, 2)))
        except NoUpgradeRequiredError as ex:
            logger.warning(ex)
        except Exception as ex:
            import traceback;traceback.print_exc()
            logger.error(ex)
            bak_file = '{0}.bak'.format(self.cve_cpe_db)
            if os.path.isfile(bak_file):
                shutil.move(bak_file, self.cve_cpe_db)
        finally:
            bak_file = '{0}.bak'.format(self.cve_cpe_db)
            if os.path.isfile(bak_file):
                os.unlink(bak_file)
