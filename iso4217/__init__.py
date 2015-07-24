""":mod:`iso4217` --- ISO 4217 currency data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import datetime
import enum
try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree

from pkg_resources import resource_string

__all__ = ('Currency', '__published__', '__version__', '__version_info__',
           'raw_table', 'raw_xml')


raw_xml = etree.fromstring(resource_string(__name__, 'table_a1.xml'))
__published__ = datetime.date(*map(int, raw_xml.attrib['Pblshd'].split('-')))
__version_prefix__ = (1, 0)
__version_info__ = (__version_prefix__ +
                    (int(__published__.strftime('%Y%m%d')),))
__version__ = '.'.join(map(str, __version_info__))


def parse_table(tree):
    """Parse an ISO 4217 XML table data and then return raw table as
    a list of dictionaries.

    """
    table = []
    for node in tree.findall('CcyTbl/CcyNtry'):
        ctry_nm = node.find('CtryNm')
        if ctry_nm is not None:
            ctry_nm = ctry_nm.text.strip()
        ccy_nm = node.find('CcyNm')
        if ccy_nm is not None:
            ccy_nm = ccy_nm.text.strip()
        ccy = node.find('Ccy')
        if ccy is not None:
            ccy = ccy.text.strip()
        ccy_nbr = node.find('CcyNbr')
        if ccy_nbr is not None:
            ccy_nbr = int(ccy_nbr.text.strip())
        ccy_mnr_unts = node.find('CcyMnrUnts')
        if ccy_mnr_unts is not None:
            ccy_mnr_unts = ccy_mnr_unts.text.strip()
        table.append({
            'CtryNm': ctry_nm,
            'CcyNm': ccy_nm,
            'Ccy': ccy,
            'CcyNbr': ccy_nbr,
            'CcyMnrUnts': ccy_mnr_unts,
        })
    return table


#: (:class:`collections.abc.Sequence`) The raw table list.
raw_table = parse_table(raw_xml)


def update_enum_dict(locals_, taw_table):
    """Since :mod:`enum` module's class-level locals dictionary is
    not an ordinary Python :class:`dict`, so leaking local variables
    make unexpected behaviors.

    This function takes a ``locals_`` dictionary and then add
    all available enumerants to this.

    """
    enumerants = {}
    for _ccy_ntry in raw_table:
        if _ccy_ntry['CcyNbr'] is None:
            continue
        if not _ccy_ntry.get('CcyMnrUnts', '').isdigit():
            continue
        code = _ccy_ntry['Ccy']
        lcode = code.lower()
        if lcode in ('mro',):
            lcode += '_'
        if lcode in enumerants:
            enumerants[lcode][3].add(_ccy_ntry['CtryNm'])
            continue
        enumerants[lcode] = (
            code,
            int(_ccy_ntry['CcyNbr']),
            _ccy_ntry['CcyNm'],
            set([_ccy_ntry['CtryNm']]),
            int(_ccy_ntry['CcyMnrUnts']),
        )
    for code, enumerant in enumerants.items():
        locals_[code] = tuple(
            frozenset(field) if isinstance(field, set) else field
            for field in enumerant
        )


class Currency(enum.Enum):
    """ISO 4217 currency.  Its enumerants are ISO 4217 currencies except for
    some special currencies like ```XXX``.  Enumerants names are lowercase
    cureency code e.g. :attr:`Currency.eur`, :attr:`Currency.usd`.

    """

    update_enum_dict(locals(), raw_table)

    def __init__(self, code, number, currency_name, country_names, exponent):
        self.code = code
        self.number = number
        self.currency_name = currency_name
        self.country_names = country_names
        self.exponent = exponent
