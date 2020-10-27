
import datetime
import json
import logging
from typing import Callable, TypeVar
from sobers.config import OUT_ATTRS

logger = logging.getLogger(__name__)


class BaseInputPlugin:
    """Converts a given row (string) to list of types defined by input schema"""
    def __init__(self, schema: tuple, separator=","):
        """Converts a single row of CSV to Type aware list of values based on provided schema

        :param schema: schema corresponds to each attribute in the csv row
        """
        self.schema = schema
        self.separator = separator

    def __repr__(self):
        return f'{self.__class__.__name__}(schema={self.schema}, separator={self.separator})'

    def process(self, row: str):
        if not row:
            raise ValueError('Must be a valid csv row, found None')

        row_vals = row.split(self.separator)

        if len(row_vals) != len(self.schema):
            raise ValueError('Row Length and Value Length must match')

        return [schema(val) for schema, val in zip(self.schema, row_vals)]


class BaseOutputPlugin:
    """Base Output Plugin, Use it with mixin classes to create

    Use with Mixin Classes to define output type other than list, such as CSV or JSON
    """
    def __init__(self, schema: tuple, **kwargs):
        self.schema = schema
        self.kwargs = kwargs

    def __repr__(self):
        return f'{self.__class__.__name__}(schema={self.schema}, kwargs={self.kwargs})'

    def validate(self, row: list):
        """Basic validation, add if necessary"""
        if len(row) != len(self.schema):
            raise ValueError('Row Length and Value Length must match')


# need to define these to use type hinting for polymorphism
InputPluginType = TypeVar('InputPluginType', bound='A')
OutputPluginType = TypeVar('OutputPluginType', bound='A')


class CSVMixin:
    """Mixin for outputing in CSV format"""
    kwargs: dict
    validate: callable

    def output(self, row: list):

        self.validate(row)
        
        # convert all elems to string
        row = [str(field) for field in row]
        
        # single line 
        return self.kwargs.get('separator').join(row)


class JsonMixin:
    """ Mixin for outputing in JSON format"""
    validate: callable

    def output(self, row: list):

        self.validate(row)

        out = dict()
        for key, val in zip(OUT_ATTRS, row):
            if isinstance(val, datetime.date):
                val = str(val)
            out[key] = val
        return json.dumps(out)


class CSVOutPlugin(BaseOutputPlugin, CSVMixin):

    def __init__(self, schema: tuple, separator=","):
        super().__init__(schema, separator=separator)
        self.separator = separator

    def __repr__(self):
        return f'{self.__class__.__name__}(schema={self.schema}, separator={self.separator})'


class JsonOutPlugin(BaseOutputPlugin, JsonMixin):

    def __init__(self, schema: tuple):
        super().__init__(schema)

    def __repr__(self):
        return f'{self.__class__.__name__}(schema={self.schema})'


class Transformation:
    """Transform a row into another

    Transformation is defined by three values:
    - input plugin that parses csv row to types and enforces checks and schemas,
    - transformation function to apply custom logic per row, such as reordering, or merging columns
    - output plugin that converts the output of transformation function into csv row
    """
    def __init__(self,
                 input_plugin: InputPluginType,
                 transformation_func: Callable,
                 output_plugin: OutputPluginType):

        self.input_plugin = input_plugin
        self.transformation_func = transformation_func
        self.output_plugin = output_plugin

    def __repr__(self):
        return f"{self.__class__.__name__}(iplugin={self.input_plugin}, " \
               f"func={self.transformation_func}, oplugin={self.output_plugin})"

    def __call__(self, row: str):
        """Convert an input stream to output stream

        :param row:
        """
        parsed_input = self.input_plugin.process(row)
        transformed = self.transformation_func(parsed_input)
        return self.output_plugin.output(transformed)
