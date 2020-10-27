"""Types defined used in schema"""
import datetime
import logging
from typing import Optional, Union, Any

logger = logging.getLogger(__name__)


class IntType:
    """Integer type to use in schema, automatically converts that field from str integer with validation"""

    def __init__(self, nullable: bool = False):
        self.nullable = nullable

    def __repr__(self):
        return f'{self.__class__.__name__}(nullable={self.nullable})'

    def __call__(self, value) -> Optional[int]:
        if not value:
            if self.nullable:
                return None
            raise ValueError('Cannot accept None value, set nullable=True')

        return int(value)


class StrType:
    """Str type check for schema"""

    def __init__(self, nullable: bool = False):
        self.nullable = nullable

    def __repr__(self):
        return f'{self.__class__.__name__}(nullable={self.nullable})'

    def __call__(self, value) -> Optional[str]:
        if not value:
            if self.nullable:
                return None
            raise ValueError('Cannot accept None value, set nullable=True')

        return str(value)


class FloatType:
    """Float type to use in schema, automatically converts that field from str integer with validation"""

    def __init__(self, nullable: bool = False):
        self.nullable = nullable

    def __repr__(self):
        return f'{self.__class__.__name__}(nullable={self.nullable})'

    def __call__(self, value) -> Optional[float]:
        if not value:
            if self.nullable:
                return None
            raise ValueError('Cannot accept None value, set nullable=True')

        return float(value)


class DateType:
    """Date type to use in schema, converts a field from str to datetime.date vs datetime.date to str with validation"""

    def __init__(self, fmt: Optional[str] = None, nullable: bool = False):
        """DateTime Format

        :param fmt: specify a fomratter to convert str to datetime.date
        """
        self.fmt = fmt
        self.nullable = nullable

    def __repr__(self):
        return f'{self.__class__.__name__}(fmt={self.fmt}, nullable={self.nullable})'

    def __call__(self, value: Union[str, datetime.date]) -> Union[datetime.date, str, None]:
        if not value:
            if self.nullable:
                return None
            raise ValueError('Cannot accept None value, set nullable=True')

        # This is to convert datettime.date to str, used in out_schema
        if isinstance(value, datetime.date):
            return str(value)

        return datetime.datetime.strptime(value, self.fmt).date()


class EnumType:
    """Enforces a list of elements as valid values, doesn't enforce type check"""

    def __init__(self, valid_values: tuple, nullable: bool = False):
        self.valid_values = set(valid_values)
        self.nullable = nullable

    def __repr__(self):
        return f'{self.__class__.__name__}(valid_values={self.valid_values}, nullable={self.nullable})'

    def __call__(self, value) -> Any:
        if not value:
            if self.nullable:
                return None
            raise ValueError('Cannot accept None value, set nullable=True')

        if value not in self.valid_values:
            raise ValueError(f'{value} not in valid types of {self.valid_values}')
        return value
