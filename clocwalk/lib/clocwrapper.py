#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys

from clocwalk.lib.data import logger


class ClocCode(object):

    def __init__(self, search_path=('cloc', '/usr/bin/cloc', '/usr/local/bin/cloc')):
        """

        :param search_path:
        :returns: nothing

        """
        self.search_path = ''
        self._scan_result = {}
        self._last_output = ''
        self.version = ''
        self._args = ''
        self._result = ''
        self._result = ''

        for path in search_path:
            try:
                if sys.platform.startswith('freebsd') or sys.platform.startswith('linux') or sys.platform.startswith(
                    'darwin'):
                    p = subprocess.Popen(
                        [path, '--version'],
                        bufsize=10000,
                        stdout=subprocess.PIPE,
                        close_fds=True
                    )
                else:
                    p = subprocess.Popen(
                        [path, '--version'],
                        bufsize=10000,
                        stdout=subprocess.PIPE
                    )

            except OSError:
                pass
            else:
                self._cloc_path = path
                break
        else:
            raise Exception(
                'cloc program was not found in path. PATH is : {0}'.format(os.getenv('PATH'))
            )

        self._last_output = bytes.decode(p.communicate()[0])
        self.version = self._last_output

    @property
    def get_last_output(self):
        """
        :returns:
        """
        return self._last_output

    @property
    def cloc_version(self):
        """
        :returns:
        """
        return self.version

    @property
    def command_line(self):
        """
        """

        return self._args

    @property
    def result(self):
        """
        """
        return self._result

    def start(self, **kwargs):
        """
        :param kwargs:

        :returns:
        """
        _args = kwargs.get('args', None)
        assert not _args is list, 'args must be a list!'

        code_dir = kwargs.get('code_dir', None)
        args = [self._cloc_path, '--json', '-'] + _args + [code_dir]
        logger.debug('Scan parameters: "{0}"'.format(' '.join(args)))
        self._args = ' '.join(args)

        p = subprocess.Popen(
            args,
            bufsize=100000,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self._last_output, _err = p.communicate()
        self._result = bytes.decode(self._last_output)
        _err = bytes.decode(_err)

        return self._result, _err
