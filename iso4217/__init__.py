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


raw_xml = etree.fromstring(resource_string(__name__, 'table.xml'))
__published__ = datetime.date(*map(int, raw_xml.attrib['Pblshd'].split('-')))
__version_prefix__ = (1, 5)
__version_info__ = (__version_prefix__ +
                    (int(__published__.strftime('%Y%m%d')),))
__version__ = '.'.join(map(str, __version_info__))


def parse_table(tree):
    """Parse an ISO 4217 XML table data and then return raw table as
    a dictionary.

    """
    table = {}
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
        try:
            ccy_dict = table[ccy]
        except KeyError:
            table[ccy] = {
                'CtryNm': set([ctry_nm]),
                'CcyNm': ccy_nm,
                'Ccy': ccy,
                'CcyNbr': ccy_nbr,
                'CcyMnrUnts': ccy_mnr_unts,
            }
        else:
            ccy_dict['CtryNm'].add(ctry_nm)
    return table


#: (:class:`collections.abc.Mapping`) The raw table.
raw_table = parse_table(raw_xml)


def update_enum_dict(locals_, raw_table):
    """Since :mod:`enum` module's class-level locals dictionary is
    not an ordinary Python :class:`dict`, so leaking local variables
    make unexpected behaviors.

    This function takes a ``locals_`` dictionary and then add
    all available enumerants to this.

    """
    enumerants = {}
    for code, _ccy_ntry in raw_table.items():
        if _ccy_ntry['CcyNbr'] is None:
            continue
        if not _ccy_ntry.get('CcyMnrUnts', '').isdigit():
            continue
        lcode = code.lower()
        if lcode in ('mro',):
            lcode += '_'
        enumerants[lcode] = code
    for code, enumerant in enumerants.items():
        locals_[code] = enumerant


class Currency(enum.Enum):
    """ISO 4217 currency.  Its enumerants are ISO 4217 currencies except for
    some special currencies like ```XXX``.  Enumerants names are lowercase
    cureency code e.g. :attr:`Currency.eur`, :attr:`Currency.usd`.

    """

    update_enum_dict(locals(), raw_table)

    @property
    def code(self):
        """(:class:`str`) The currency code which consist of 3 uppercase
        characters e.g. ``'USD'``, ``'EUR'``.

        """
        return self.value

    @property
    def number(self):
        """(:class:`int`) The currency number."""
        return int(raw_table[self.value]['CcyNbr'])

    @property
    def currency_name(self):
        """(:class:`str`) The human-readable name of the currency e.g.
        ``'US Dollar'``, ``'Euro'``.

        """
        return raw_table[self.value]['CcyNm']

    @property
    def country_names(self):
        return frozenset(raw_table[self.value]['CtryNm'])

    @property
    def exponent(self):
        """(:class:`int`) The treatment of minor currency unit, in exponent
        where base is 10.  For example, a U.S. dollar is 100 cents,
        so ``Currency.usd.exponent == 2``.

        There are also currencies that have no minor ucrrency unit.
        These are represented as 0.

        """
        return int(raw_table[self.value]['CcyMnrUnts'])
