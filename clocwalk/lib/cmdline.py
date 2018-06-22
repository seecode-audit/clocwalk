#!/usr/bin/env python
# coding: utf-8

import os
import sys

import clocwalk

from optparse import OptionError
from optparse import OptionParser

from clocwalk.lib.common import getUnicode
from clocwalk.lib.data import logger
from clocwalk.lib.data import conf
from clocwalk.lib.settings import IS_WIN


def cmdLineParser():
    """
    This function parses the command line parameters and arguments
    """

    _ = getUnicode(os.path.basename(sys.argv[0]), encoding=sys.getfilesystemencoding())

    usage = "%s [options]" % "clocwalk"

    parser = OptionParser(usage=usage)

    try:
        parser.add_option("-v", dest="verbose", type="int", default=1,
                          help="Verbosity level: 0-3 (default 1)")

        parser.add_option('-p', '--code-dir', dest='code_dir', help='Code path or directory')
        parser.add_option('--skip-check-newver',dest='skip_check_new_version', action='store_true',
                          default=False, help='Skip detection of new version components (default False).')

        parser.add_option('--exclude-ext', dest='exclude_ext', help='Does not include file extensions')
        parser.add_option('--exclude-dir', dest='exclude_dir', help='Does not contain directories')

        parser.add_option("--timeout", dest="timeout", type="int", default=5,
                          help="Http request timeout (default 5)")

        parser.add_option('--version', '-V', dest='version', action='store_true',
                          default=False, help='Print out the version')

        argv = []
        for arg in sys.argv:
            argv.append(getUnicode(arg, encoding=sys.getfilesystemencoding()))

        try:
            (args, _) = parser.parse_args(argv)

            if not any((args.version, args.code_dir)):
                errMsg = "missing a mandatory option (-p, --version)"
                errMsg += "use -h for help"
                raise SystemExit(errMsg)

            if args.version:
                print "clocwalk v%s" % clocwalk.__version__
                raise SystemExit

            conf.update(args.__dict__)

        except UnicodeEncodeError, ex:
            print "\n[!] %s" % ex.object.encode("unicode-escape")
            raise SystemExit

        except SystemExit:
            raise

    except (OptionError, TypeError), e:
        parser.error(e)

    except SystemExit:
        if IS_WIN:
            print "\nPress Enter to continue...",
            raw_input()
        raise

    logger.debug("parsing command line")
