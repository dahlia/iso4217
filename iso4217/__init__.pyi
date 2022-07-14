import datetime
import enum
from typing import AbstractSet, Mapping, Optional, Tuple, Union
from xml.etree import ElementTree as etree


__published__: datetime.date = ...
__version__: str = ...
__version_info__: Tuple[int, int, int] = ...

raw_xml: etree.Element
raw_table: Mapping[str, Mapping[str, Union[AbstractSet[str], str, int]]] = ...


class Currency(enum.Enum):

    @property
    def code(self) -> str: ...

    @property
    def number(self) -> int: ...

    @property
    def currency_name(self) -> str: ...

    @property
    def country_names(self) -> AbstractSet[str]: ...

    @property
    def exponent(self) -> Optional[int]: ...
