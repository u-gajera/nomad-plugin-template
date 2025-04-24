# from nomad.config.models.plugins import ParserEntryPoint
# from pydantic import Field


# class NewParserEntryPoint(ParserEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')

#     def load(self):
#         from nomad_battery_data.parsers.parser import NewParser

#         return NewParser(**self.model_dump())


# parser_entry_point = NewParserEntryPoint(
#     name='NewParser',
#     description='New parser entry point configuration.',
#     mainfile_name_re=r'.*\.newmainfilename',
# )

from nomad.config.models.plugins import ParserEntryPoint
from .parser import BatteryDataParser

battery_data_parser = ParserEntryPoint(
    name='Battery Parcer from CSV file',
    description='Parses tabular battery data CSV into the BatteryProperties schema.',
    mainfile_name_re=r'.*\.csv$'
)

def load():
    # Pass any entry‑point kwargs (none here) into the parser
    return BatteryDataParser(**battery_data_parser.dict())
