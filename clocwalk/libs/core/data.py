# coding: utf-8

import os
import shutil

from clocwalk.libs.core.datatype import AttribDict
from clocwalk.libs.core.db_helper import DBHelper
from clocwalk.libs.core.log import LOGGER
from clocwalk.libs.core.settings import PYVERSION

# paths
paths = AttribDict()
paths.ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

home_path = None
if PYVERSION == 2:
    home_path = os.path.expanduser('~')
else:
    from pathlib import Path
    home_path = Path.home()

work_path = os.path.join(home_path, '.clocwalk')

if not os.path.isdir(work_path):
    try:
        os.makedirs(work_path)
    except:
        work_path = '/usr/local/clocwalk'
        os.makedirs(work_path)
    if not os.path.isfile(os.path.join(work_path, 'conf.yaml')):
        shutil.copy(os.path.join(paths.ROOT_PATH, 'conf.yaml'), os.path.join(work_path, 'conf.yaml'))

paths.WORK_PATH = work_path
paths.PLUGINS_PATH = os.path.join(paths.ROOT_PATH, "libs", 'analyzer')
paths.CONFIG_FILE = os.path.join(paths.WORK_PATH, 'conf.yaml')
paths.DB_FILE = os.path.join(paths.WORK_PATH, 'db', 'cve_cpe.db')
paths.CACHE_PATH = os.path.join(paths.WORK_PATH, 'db', 'cache')
paths.CVE_CACHE_PATH = os.path.join(paths.CACHE_PATH, 'cve')
paths.HTTP_CACHE_PATH = os.path.join(paths.CACHE_PATH, 'http')
paths.CVE_PATH = os.path.join(paths.WORK_PATH, 'db', 'json')

# object to share within function and classes command
# line options and settings
conf = AttribDict()
conf.verbose = 1
conf.config = None
conf.output = None
conf.force_update = False
conf.upgrade_interval = "7d"
conf.skip_check_new_version = True

# object to share within function and classes results
kb = AttribDict()
kb.pluginFunctions = []
kb.cpe_cache = None  # CPE
kb.db = None
kb.http_cache = None
kb.dependencies = {}

# logger
logger = LOGGER

try:
    kb.db = DBHelper(paths.DB_FILE)
except Exception as ex:
    logger.warn(ex)
