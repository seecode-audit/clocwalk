# coding: utf-8

import os
import platform
import sys

from clocwalk import __version__

DESCRIPTION = "xsseroot#gmail.com"

# colorful banner
BANNER = """==============================================================

_________ .__                               .__   __    
\_   ___ \|  |   ____   ______  _  _______  |  | |  | __
/    \  \/|  |  /  _ \_/ ___\ \/ \/ /\__  \ |  | |  |/ /
\     \___|  |_(  <_> )  \___\     /  / __ \|  |_|    < 
 \______  /____/\____/ \___  >\/\_/  (____  /____/__|_ \\
        \/                 \\/             \/          \/\n
        clocwalk v%s %s\n==============================================================
""" % (__version__, DESCRIPTION)

# System variables
IS_WIN = platform.system()

# The name of the operating system dependent module imported. The following names have currently
#  been registered: 'posix', 'nt', 'mac', 'os2', 'ce', 'java', 'riscos'
PLATFORM = os.name
PYVERSION = sys.version.split()[0]
