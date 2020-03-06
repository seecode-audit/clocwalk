clocwalk
================

Project code and dependent component analysis tools.

.. image:: https://travis-ci.com/MyKings/clocwalk.svg?branch=master
    :target: https://travis-ci.com/MyKings/clocwalk

.. image:: https://badge.fury.io/py/clocwalk.svg
    :target: https://badge.fury.io/py/clocwalk

.. image:: https://img.shields.io/badge/python-2.7|3.6|3.7-brightgreen.svg
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

Dependent installation
-------------------------

::

  npm install -g cloc                    # https://www.npmjs.com/package/cloc
  sudo apt install cloc                  # Debian, Ubuntu
  sudo yum install cloc                  # Red Hat, Fedora
  sudo dnf install cloc                  # Fedora 22 or later
  sudo pacman -S cloc                    # Arch
  sudo emerge -av dev-util/cloc          # Gentoo https://packages.gentoo.org/packages/dev-util/cloc
  sudo apk add cloc                      # Alpine Linux
  sudo pkg install cloc                  # FreeBSD
  sudo port install cloc                 # Mac OS X with MacPorts
  brew install cloc                      # Mac OS X with Homebrew
  choco install cloc                     # Windows with Chocolatey
  scoop install cloc                     # Windows with Scoop


Install
----------

::
  
  pip setup.py install


Usage
----------

::

    from cloclwalk import ClocDetector
    from cloclwalk import query_cve

    def test():
        c = ClocDetector(
            code_dir='/tmp/sample_project',
            enable_vuln_scan=True,
            enable_upgrade=True,
        )
        c.start()
        print(c.getResult())
    
    if __name__ == '__main__':
        test()
        print(query_cve("CVE-2020-0608"))

CLI
-----------

::
  
  $ python cli.py --vuln-scan -p /data/seecode/tasks/7230/vuln_project-master/


::

    ==============================================================
    
    _________ .__                               .__   __
    \_   ___ \|  |   ____   ______  _  _______  |  | |  | __
    /    \  \/|  |  /  _ \_/ ___\ \/ \/ /\__  \ |  | |  |/ /
    \     \___|  |_(  <_> )  \___\     /  / __ \|  |_|    <
     \______  /____/\____/ \___  >\/\_/  (____  /____/__|_ \
            \/                 \/             \/          \/
    
            clocwalk v2.0.0 xsseroot#gmail.com
    ==============================================================
    
    [17:45:02] [INFO] 4 analyzer plugin loaded.
    [17:45:02] [INFO] analysis statistics code ...
    [17:45:03] [INFO] Start using CPE rules for matching ...
    [17:45:03] [INFO] [-] Start analysis "/data/seecode/tasks/7230/vuln_project-master/pom.xml" file...
    [17:45:03] [INFO] [-] Start analysis "/data/seecode/tasks/7230/vuln_project-master/src/pom.xml" file...
    [17:45:03] [INFO] Start using CPE rules for matching ...
    [17:45:05] [INFO] Start using CPE rules for matching ...
    [17:45:05] [INFO] Start using CPE rules for matching ...
    {'cloc': {'Java': {'blank': 9, 'code': 244, 'comment': 21, 'nFiles': 2},
              'Maven': {'blank': 6, 'code': 67, 'comment': 0, 'nFiles': 2},
              'Python': {'blank': 9, 'code': 106, 'comment': 3, 'nFiles': 2},
              'SUM': {'blank': 24, 'code': 417, 'comment': 24, 'nFiles': 6},
              'header': {'cloc_url': 'github.com/AlDanial/cloc',
                         'cloc_version': '1.82',
                         'elapsed_seconds': 0.254485845565796,
                         'files_per_second': 23.5769497775417,
                         'lines_per_second': 1827.21360775948,
                         'n_files': 6,
                         'n_lines': 465}},
     'depends': [{'Java': [{'cve': {'CVE-2017-18349': 'parseObject in Fastjson '
                                                      'before 1.2.25, as used in '
                                                      'FastjsonEngine in Pippo '
                                                      '1.11.0 and other products, '
                                                      'allows remote attackers to '
                                                      'execute arbitrary code via '
                                                      'a crafted JSON request, as '
                                                      'demonstrated by a crafted '
                                                      'rmi:// URI in the '
                                                      'dataSourceName field of '
                                                      'HTTP POST data to the Pippo '
                                                      '/json URI, which is '
                                                      'mishandled in '
                                                      'AjaxApplication.java.'},
                            'new_version': '',
                            'origin_file': '/data/seecode/tasks/7230/vuln_project-master/pom.xml',
                            'parent_file': '',
                            'product': 'fastjson',
                            'vendor': 'com.alibaba',
                            'version': '1.2.8'},
                           {'cve': {},
                            'new_version': '',
                            'origin_file': '/data/seecode/tasks/7230/vuln_project-master/pom.xml',
                            'parent_file': '',
                            'product': 'spring-core',
                            'vendor': 'org.springframework',
                            'version': '4.3.12.RELEASE'},
                           {'cve': {},
                            'new_version': '',
                            'origin_file': '/data/seecode/tasks/7230/vuln_project-master/pom.xml',
                            'parent_file': '',
                            'product': 'solr-solrj',
                            'vendor': 'org.apache.solr',
                            'version': '5.5.3'},
                           {'cve': {},
                            'new_version': '',
                            'origin_file': '/data/seecode/tasks/7230/vuln_project-master/pom.xml',
                            'parent_file': '',
                            'product': 'shiro-core',
                            'vendor': 'org.apache.shiro',
                            'version': '1.2.4'},
                           {'cve': {'CVE-2017-15095': 'A deserialization flaw was '
                                                      'discovered in the '
                                                      'jackson-databind in '
                                                      'versions before 2.8.10 and '
                                                      '2.9.1, which could allow an '
                                                      'unauthenticated user to '
                                                      'perform code execution by '
                                                      'sending the maliciously '
                                                      'crafted input to the '
                                                      'readValue method of the '
                                                      'ObjectMapper. This issue '
                                                      'extends the previous flaw '
                                                      'CVE-2017-7525 by '
                                                      'blacklisting more classes '
                                                      'that could be used '
                                                      'maliciously.'},
                            'new_version': '',
                            'origin_file': '/data/seecode/tasks/7230/vuln_project-master/src/pom.xml',
                            'parent_file': '/data/seecode/tasks/7230/vuln_project-master/pom.xml',
                            'product': 'jackson-databind',
                            'vendor': 'com.fasterxml.jackson.core',
                            'version': '2.8.4'}]}]}
    [17:45:05] [INFO] Total time consumption: 3.34(s)
