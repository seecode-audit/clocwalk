# coding: utf-8

import os
import sys
import subprocess

from clocwalk import __version__


DESCRIPTION = "Project code and dependent component analysis tools."

# colorful banner
BANNER = """        Clocwalk v%s \n  %s
""" % (__version__, DESCRIPTION)

# System variables
IS_WIN = subprocess.mswindows

# The name of the operating system dependent module imported. The following names have currently been registered: 'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'
PLATFORM = os.name
PYVERSION = sys.version.split()[0]

# Encoding used for Unicode data
UNICODE_ENCODING = "utf8"

# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\?%02x"
