clocwalk
================

Project code and dependent component analysis tools.

.. image:: https://travis-ci.com/MyKings/clocwalk.svg?branch=master
    :target: https://travis-ci.com/MyKings/clocwalk

.. image:: https://badge.fury.io/py/clocwalk.svg
    :target: https://badge.fury.io/py/clocwalk

.. image:: https://img.shields.io/badge/python-2.6|2.7-brightgreen.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/github/issues/MyKings/clocwalk.svg
    :alt: GitHub issues
    :target: https://github.com/MyKings/clocwalk/issues


.. image:: https://img.shields.io/github/forks/MyKings/clocwalk.svg
    :alt: GitHub forks
    :target: https://github.com/MyKings/clocwalk/network


.. image:: https://img.shields.io/github/stars/MyKings/clocwalk.svg
    :alt: GitHub stars
    :target: https://github.com/MyKings/clocwalk/stargazers


.. image:: https://img.shields.io/github/license/MyKings/clocwalk.svg
    :alt: GitHub license
    :target: https://github.com/MyKings/clocwalk/blob/master/LICENSE


Install
----------

::
  
  pip install clocwalk


Usage
----------

::

    from cloclwalk import ClocDetector
    
    def test():
        c = ClocDetector(code_dir='/tmp/sample_project')
        c.start()
        print c.result
    
    if __name__ == '__main__':
        test()

CLI
-----------

::
  
  $ python cli.py -p /tmp/clocwalk


::
    
            Clocwalk v0.1.0
      Project code and dependent component analysis tools.
    
    [15:38:50] [INFO] 4 fingerprints plugin loaded.
    [15:38:50] [INFO] checking depends ...
    [15:38:50] [INFO] analysis statistics code ...
    {'cloc': {u'C': {u'blank': 671, u'code': 2418, u'comment': 297, u'nFiles': 3},
              u'C Shell': {u'blank': 12,
                           u'code': 17,
                           u'comment': 7,
                           u'nFiles': 1},
              u'C/C++ Header': {u'blank': 1982,
                                u'code': 13064,
                                u'comment': 6219,
                                u'nFiles': 81},
              u'CSS': {u'blank': 736,
                       u'code': 3568,
                       u'comment': 464,
                       u'nFiles': 34},
              u'Fish Shell': {u'blank': 16,
                              u'code': 47,
                              u'comment': 13,
                              u'nFiles': 1},
              u'HTML': {u'blank': 142,
                        u'code': 1419,
                        u'comment': 6,
                        u'nFiles': 41},
              u'INI': {u'blank': 1, u'code': 3, u'comment': 0, u'nFiles': 1},
              u'JSON': {u'blank': 0, u'code': 362, u'comment': 0, u'nFiles': 66},
              u'JavaScript': {u'blank': 5148,
                              u'code': 49720,
                              u'comment': 2630,
                              u'nFiles': 33},
              u'Maven': {u'blank': 9, u'code': 221, u'comment': 0, u'nFiles': 2},
              u'PO File': {u'blank': 7, u'code': 27, u'comment': 8, u'nFiles': 2},
              u'Python': {u'blank': 133897,
                          u'code': 587161,
                          u'comment': 188640,
                          u'nFiles': 3216},
              u'SUM': {u'blank': 143463,
                       u'code': 664447,
                       u'comment': 199996,
                       u'nFiles': 3700},
              u'TeX': {u'blank': 88,
                       u'code': 1602,
                       u'comment': 603,
                       u'nFiles': 6},
              u'Visual Basic': {u'blank': 23,
                                u'code': 186,
                                u'comment': 0,
                                u'nFiles': 2},
              u'Windows Resource File': {u'blank': 10,
                                         u'code': 153,
                                         u'comment': 0,
                                         u'nFiles': 54},
              u'XML': {u'blank': 15,
                       u'code': 1503,
                       u'comment': 5,
                       u'nFiles': 130},
              u'XSLT': {u'blank': 605,
                        u'code': 2347,
                        u'comment': 1095,
                        u'nFiles': 7},
              u'YAML': {u'blank': 96, u'code': 607, u'comment': 9, u'nFiles': 19},
              u'header': {u'cloc_url': u'github.com/AlDanial/cloc',
                          u'cloc_version': u'1.76',
                          u'elapsed_seconds': 9.26226902008057,
                          u'files_per_second': 399.470150562288,
                          u'lines_per_second': 108818.476100712,
                          u'n_files': 3700,
                          u'n_lines': 1007906},
              u'make': {u'blank': 5, u'code': 22, u'comment': 0, u'nFiles': 1}},
     'depends': [{'Python': [{'name': 'lxml',
                              'new_version': '',
                              'origin': u'requirements.txt',
                              'tag': '',
                              'version': ''},
                             {'name': 'requests',
                              'new_version': '',
                              'origin': u'requirements.txt',
                              'tag': '',
                              'version': ''},
                             {'name': 'PyYAML',
                              'new_version': '',
                              'origin': u'requirements.txt',
                              'tag': '',
                              'version': ''}]}]}
