import pytest
import datetime
from sobers.sober_types import DateType, IntType, FloatType, EnumType
from sobers.plugins import BaseInputPlugin, CSVOutPlugin, JsonOutPlugin


@pytest.fixture
def schemas():
    return {
        'input': (DateType('%d %b %Y'), EnumType(('add', 'remove')), IntType(), IntType(), IntType(), IntType()),
        'output': (DateType(), EnumType(('add', 'remove')), FloatType(), IntType(), IntType())
    }


def test_base_input_plugin(schemas):
    """Input plugin should parse and create type aware lists"""

    # date_readable 	type 	euro 	cents 	to 	    from
    # 6 Oct 2019 	    add 	1060 	8 	    198 	188

    row = "6 Oct 2019,add,1060,8,198,188"

    in_plugin = BaseInputPlugin(schema=schemas.get('input'))
    processed = in_plugin.process(row)

    expected = [datetime.date(2019, 10, 6), 'add', 1060, 8, 198, 188]

    assert expected == processed


def test_base_csv_output_plugin(schemas):
    """CSVOutputPlugin should convert a given list to a string with validation"""

    row = [datetime.date(2019, 10, 6), 'add', 1060.2, 198, 188]
    processed_hyphen = CSVOutPlugin(schema=schemas.get('output'), separator="-").output(row)
    processed_comma = CSVOutPlugin(schema=schemas.get('output'), separator=",").output(row)

    assert processed_hyphen == '2019-10-06-add-1060.2-198-188'
    assert processed_comma == '2019-10-06,add,1060.2,198,188'


def test_base_json_output_plugin(schemas):
    """JsonOutputPlugin should convert a given list to a string with validation"""

    row = [datetime.date(2019, 10, 6), 'add', 1060.2, 198, 188]
    processed = JsonOutPlugin(schema=schemas.get('output')).output(row)

    assert processed == '{"date": "2019-10-06", "type": "add", "amount": 1060.2, "from": 198, "to": 188}'
