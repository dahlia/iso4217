import datetime
import enum
from typing import (
    AbstractSet,
    Any,
    Callable,
    Generator,
    Mapping,
    Optional,
    Tuple,
    Union,
)
from xml.etree import ElementTree as etree


__published__: datetime.date = ...
__version__: str = ...
__version_info__: Tuple[int, int, int] = ...

raw_xml: etree.Element
raw_table: Mapping[str, Mapping[str, Union[AbstractSet[str], str, int]]] = ...


class Currency(enum.Enum):

    @classmethod
    def _validate(cls, value: Any) -> "Currency": ...

    # Pydantic v1 support
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]: ...

    # Pydantic v2 support
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> Any: ...

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
