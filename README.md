
## SOBERS assignment solution

`sobers-console` is a command line tool to parse, validate and standardize the input CSV files.

### Introduction

Out of the box `sobers-console` can parse/transform three different CSV files defined in assignment
and more transformers can be defined easily. 

#### Plugin Based Architecture

Row based processing is done using three components:
 - Input Plugin (such as `sobers.plugins.BaseInputPlugin`)
 - User defined transform function for row based operations(such as `sobers.config.bank3_mapping`)
 - Output Plugin (such as `sobers.plugins.CSVOutPlugin` or `sobers.plugins.JsonOutPlugin`)

This plugin architecture allows to seperate out different concerns and allows plugable architecture.
For example, instead of writing as CSV, we can output in JSON format using `JsonOutPlugin`

All these Plugins are joined using `sobers.plugins.Transformation` class, and for each account/bank these 
transformations can be saved to a constants file to use later in command line 
(such as `sobers.constants.bank3_csv_stream` defines all plugins + transformations for bank3 format)

# Installation

After pulling from git,

```bash
#> cd sobers && pip install .
```
will install sobers package

### Console Usage

Takes a source CSV file, a predefined transformation(validation as well) and output path. Optionally can add --verbose
flag for debugging

```bash
#> cat /tmp/sobers/in/test3.csv 

date_readable,type,euro,cents,to,from
5 Oct 2019,remove,5,7,182,198
6 Oct 2019,add,1060,8,198,188

#> sobers-console \
    --source-path=/tmp/sobers/in/test3.csv 
    --transformation=bank3 
    --out-path=/tmp/sobers/out

2020-10-26 21:56:37,365 36673 sobers.utils INFO: Outputted to /tmp/sobers/out/bank3.csv
2020-10-26 21:56:37,365 36673 __main__ INFO: Finished successfully

#> cat /tmp/sobers/out/bank3.csv
date,type,amount,from,to
2019-10-05,remove,5.07,198,182
2019-10-06,add,1060.08,188,198 
``` 

### Deep Dive on Transformation

Input Plugins read a row of CSV file and converts to type aware list objects
```python
from sobers.plugins import BaseInputPlugin
from sobers.sober_types import DateType, EnumType, IntType, FloatType

# below is the format of our input CSV data
 
# date_readable 	type 	euro 	cents 	to 	    from
# 6 Oct 2019 	    add 	1060 	8 	    198 	188

row = "6 Oct 2019,add,1060,8,198,188"

# define input schema
in_schema = (DateType('%d %b %Y'), EnumType(('add', 'remove')), IntType(), IntType(), IntType(), IntType())

# Create InputPlugin
in_plugin = BaseInputPlugin(in_schema)

# parse row

print(in_plugin.process(row))

>>> [datetime.date(2019, 10, 6), 'add', 1060, 8, 198, 188]
```

Transformation function is simply a user defined function 
takes the output of inputplugin (list) and rearranges/modifies/removes
fields then returns the output as another list

```python
# Row manipulation for bank 3
def bank3_mapping(row: list) -> list:
    new_row = list()
    new_row[:2] = row[:2]

    # merge euro and cents columns
    new_row.append(row[2] + 0.01*row[3])

    # add from field before to
    new_row.append(row[5])

    # add "to" field as last
    new_row.append(row[4])

    return new_row

row = [datetime.date(2019, 10, 6), 'add', 1060, 8, 198, 188]

bank3_mapping(row)

>>> [datetime.date(2019, 10, 6), 'add', 1060.08, 188, 198]
```

Output Plugin serializes to the desired format

```python
from sobers.plugins import CSVOutPlugin, JsonOutPlugin
from sobers.sober_types import DateType, EnumType, IntType, FloatType

row = [datetime.date(2019, 10, 6), 'add', 1060, 8, 198, 188]

# Create a CSV and Json output plugins
out_schema = (DateType(), EnumType(('add', 'remove')), FloatType(), IntType(), IntType())

csv_plugin = CSVOutPlugin(schema=out_schema)
json_plugin = JsonOutPlugin(schema=out_schema)

# render a CSV line
print(csv_plugin(row)) 

>>>'2019-10-06,add,1060.08,188,198'

# render a JSON
print(json_plugin(row)) 
>>> '{"date": "2019-10-06", "type": "add", "amount": 1060.08, "from": 188, "to": 198}'
```
### Putting it all together

Create a Transform object from the components above 

```python
from sobers.plugins import Transformation
csvtransform = Transformation(in_plugin, bank3_mapping, csv_plugin)
jsontransform = Transformation(in_plugin, bank3_mapping, json_plugin)

row = "6 Oct 2019,add,1060,8,198,188"
print(csvtransform(row))
>>> '2019-10-06,add,1060.08,188,198'

print(jsontransform(row)) 
>>> '{"date": "2019-10-06", "type": "add", "amount": 1060.08, "from": 188, "to": 198}'
```

Since `csvtransform` or `jsontransform` are callable objects we can store them
and call whenever needed. Therefore a specific transform for a bank/client
can be stored as a Transformation object and can be called.