"""Configs/Constants are defined here"""
from sobers.sober_types import DateType, EnumType, FloatType, IntType

# Logging format
LOGGING_FORMAT = '%(asctime)s %(process)d %(name)s %(levelname)s: %(message)s'

OUT_ATTRS = ["date", "type", "amount", "from", "to"]

# We export in this schema: Date, Type, Amount, From, To
OUT_SCHEMA = (DateType(), EnumType(('add', 'remove')), FloatType(), IntType(), IntType())

# timestamp 	type 	amount 	from 	to
# Oct 1 2019 	remove 	99.20 	198 	182
BANK_1_IN_SCHEMA = (DateType('%b %d %Y'), EnumType(('add', 'remove')), FloatType(), IntType(), IntType())

# date 	        transaction 	amounts 	to 	    from
# 03-10-2019 	remove 	        99.40 	    182 	198
BANK_2_IN_SCHEMA = (DateType('%d-%m-%Y'), EnumType(('add', 'remove')), FloatType(), IntType(), IntType())

# date_readable 	type 	euro 	cents 	to 	    from
# 5 Oct 2019 	    remove 	5 	    7 	    182 	198
BANK_3_IN_SCHEMA = (DateType('%d %b %Y'), EnumType(('add', 'remove')), IntType(), IntType(), IntType(), IntType())


# Row manipulation func for bank 1 (Identity function)
def bank1_mapping(row: list) -> list:
    return row


# Row manipulation for bank 2
def bank2_mapping(row: list) -> list:
    # Replace from and to columns
    row[3], row[4] = row[4], row[3]
    return row


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
