from sobers.plugins import Transformation, BaseInputPlugin, CSVOutPlugin
from sobers.config import BANK_1_IN_SCHEMA, BANK_3_IN_SCHEMA, BANK_2_IN_SCHEMA, OUT_SCHEMA
from sobers.config import bank1_mapping, bank2_mapping, bank3_mapping

# These are ready to use ETLs for each bank.
bank1_csv_stream = Transformation(BaseInputPlugin(BANK_1_IN_SCHEMA), bank1_mapping, CSVOutPlugin(OUT_SCHEMA))
bank2_csv_stream = Transformation(BaseInputPlugin(BANK_2_IN_SCHEMA), bank2_mapping, CSVOutPlugin(OUT_SCHEMA))
bank3_csv_stream = Transformation(BaseInputPlugin(BANK_3_IN_SCHEMA), bank3_mapping, CSVOutPlugin(OUT_SCHEMA))

streams = {
    "bank1": bank1_csv_stream,
    "bank2": bank2_csv_stream,
    "bank3": bank3_csv_stream
}
