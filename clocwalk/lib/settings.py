# coding: utf-8

import os
import sys
import platform

from clocwalk import __version__


DESCRIPTION = "Project code and dependent component analysis tools."

# colorful banner
BANNER = """        Clocwalk v%s \n  %s
""" % (__version__, DESCRIPTION)

# System variables
IS_WIN = platform.system()

# The name of the operating system dependent module imported. The following names have currently been registered: 'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'
PLATFORM = os.name
PYVERSION = sys.version.split()[0]

