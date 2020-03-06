#!/usr/bin/env python
# coding: utf-8

import os
import hashlib

try:
    import cPickle as pickle
except:
    import pickle

from clocwalk.libs.core.exception import DataException
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import paths
from clocwalk.libs.core.http import RequestConnect
from clocwalk.libs.detector.cvecpe import Cpe23Info


class AttribDictCache(dict):
    """
    This class defines the object, inheriting from Python data
    type dictionary.

    >>> foo = AttribDictCache()
    >>> foo.bar = 1
    >>> foo.bar
    1
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def get(self, item):
        return self.__getattr__(item)

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError:
            try:
                md5 = hashlib.md5()
                md5.update(item.encode('utf-8'))
                if not os.path.isdir(paths.CVE_CACHE_PATH):
                    os.makedirs(paths.CVE_CACHE_PATH)
                cache_file = os.path.join(paths.CVE_CACHE_PATH, '{0}.p'.format(md5.hexdigest()))
                if os.path.isfile(cache_file):
                    c = pickle.load(open(cache_file, "rb"))
                    dict.__setattr__(self, item, c)
                    return c
                else:
                    cpe_query_set = kb.db.query_cpe_set_by_product(product=item)
                    cpe_info_list = []
                    for cpe in cpe_query_set:
                        cve_query = kb.db.query_cve_by_cpe23uri(cpe23uri=cpe.cpe23uri)
                        cpe_info_list.append(
                            Cpe23Info(
                                uri=cpe.cpe23uri,
                                cve=cve_query,
                                vendor=cpe.vendor,
                                product=cpe.product,
                                version=cpe.version,
                                update=cpe.update_v,
                            )
                        )
                    if cpe_info_list:
                        pickle.dump(cpe_info_list, open(cache_file, "wb"))
                    dict.__setattr__(self, item, cpe_info_list)
                    return cpe_info_list
            except KeyError as ex:
                raise DataException("unable to access item '%s'" % item)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict


class AttribDictHttpCache(dict):
    """
    This class defines the object, inheriting from Python data
    type dictionary.

    >>> foo = AttribDictCache()
    >>> foo.bar = 1
    >>> foo.bar
    1
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def get(self, item):
        return self.__getattr__(item)

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError:
            try:
                md5 = hashlib.md5()
                md5.update(item.encode('utf-8'))
                if not os.path.isdir(paths.HTTP_CACHE_PATH):
                    os.makedirs(paths.HTTP_CACHE_PATH)
                cache_file = os.path.join(paths.HTTP_CACHE_PATH, '{0}.p'.format(md5.hexdigest()))
                if os.path.isfile(cache_file):
                    c = pickle.load(open(cache_file, "rb"))
                    dict.__setattr__(self, item, c)
                    return c
                else:
                    http = RequestConnect()
                    html = http.get_data(item)
                    if html:
                        pickle.dump(html, open(cache_file, "wb"))
                    dict.__setattr__(self, item, html)
                    return html
            except KeyError as ex:
                raise DataException("unable to access item '%s'" % item)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict
