import ast
import locale
import os
import os.path
import time
try:
    import urllib2
except ImportError:
    from urllib import request as urllib2
try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree
import warnings

from setuptools import setup


table_url = 'https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml'  # noqa: E501


# Override if ISO4217_DOWNLOAD_URL is set
try:
    table_url = os.environ['ISO4217_DOWNLOAD_URL']
except KeyError:
    pass


def download_table(table_url, table_filename):
    response = urllib2.urlopen(table_url)
    try:
        f = open(table_filename, 'wb')
        try:
            f.write(response.read())
        finally:
            f.close()
    finally:
        response.close()


table_filename = os.path.join(os.path.dirname(__file__),
                              'iso4217', 'table.xml')
download_flag = os.environ.get('ISO4217_DOWNLOAD')
download = (
    (
        download_flag not in ('0', 'false', 'no') and
        not os.path.isfile(table_filename)
    ) or download_flag in ('1', 'true', 'yes')
)
if download:
    download_table(table_url, table_filename)


def get_version():
    module_path = os.path.join(os.path.dirname(__file__),
                               'iso4217', '__init__.py')
    module_file = open(module_path)
    try:
        module_code = module_file.read()
    finally:
        module_file.close()
    tree = ast.parse(module_code, module_path)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, = node.targets
        if isinstance(target, ast.Name) and target.id == '__version_prefix__':
            version = '.'.join(str(e.n) for e in node.value.elts)
            break
    else:
        raise ValueError('could not find __version_prefix__')
    try:
        raw_xml = etree.parse(table_filename)
    except etree.ParseError as e:
        try:
            xml = open(table_filename)
        except IOError:
            xml_data = '(file does not exist: {})'.format(table_filename)
        else:
            xml_data = xml.read()
            xml.close()
        warnings.warn('{}\n{}'.format(e, xml_data))
        return version
    except IOError as e:
        warnings.warn(str(e))
        return version
    pblshd = raw_xml.getroot().attrib['Pblshd']
    if '-' in pblshd and ',' not in pblshd:
        pblshd_number = pblshd.replace('-', '')
    else:
        lc_time, _ = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, 'C')
        pblshd_number = \
            time.strftime("%Y%m%d", time.strptime(pblshd, "%B %d, %Y"))
        locale.setlocale(locale.LC_TIME, lc_time)
    version += '.' + pblshd_number
    return version


setup(
    version=get_version()
)
