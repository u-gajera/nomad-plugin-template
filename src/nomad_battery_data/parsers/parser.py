# from typing import (
#     TYPE_CHECKING,
# )

# if TYPE_CHECKING:
#     from nomad.datamodel.datamodel import (
#         EntryArchive,
#     )
#     from structlog.stdlib import (
#         BoundLogger,
#     )

# from nomad.config import config
# from nomad.datamodel.metainfo.workflow import Workflow
# from nomad.parsing.parser import MatchingParser

# configuration = config.get_plugin_entry_point(
#     'nomad_battery_data.parsers:parser_entry_point'
# )


# class NewParser(MatchingParser):
#     def parse(
#         self,
#         mainfile: str,
#         archive: 'EntryArchive',
#         logger: 'BoundLogger',
#         child_archives: dict[str, 'EntryArchive'] = None,
#     ) -> None:
#         logger.info('NewParser.parse', parameter=configuration.parameter)

#         archive.workflow2 = Workflow(name='test')

import re
import pandas as pd
from nomad.parsing.parser import MatchingParser
from nomad.datamodel import EntryArchive
from nomad_battery_data.schema_packages.schema_package import BatteryProperties

class BatteryDataParser(MatchingParser):
    """
    iterate and match each row to battery property.
    """
    def __init__(self):
        super().__init__(
            name='Battery CSV Parser',
            code_name='battery_csv',
            code_homepage='https://github.com/u-gajera/nomad-plugin-template'
        )

    def is_parser_for(self, file_name: str, top_level: bool = True) -> bool:
        # Only parse top-level .csv files
        return top_level and file_name.lower().endswith('.csv')

    def parse(self, mainfile: str, archive: EntryArchive, logger=None):
        """Read the CSV and populate archive.section_run 
           with BatteryProperties entries."""
        try:
            df = pd.read_csv(mainfile)
        except Exception as e:
            if logger:
                logger.error(f'BatteryCSVParser: Failed to read CSV {mainfile}: {e}')
            return

        for _, row in df.iterrows():
            # Initialize all schema fields to None
            capacity = None
            voltage = None
            coulombic_efficiency = None
            energy_density = None
            conductivity = None

            # Determine which property this row represents
            prop = str(row.get('Property', '')).strip().lower()
            num = self._to_float(row.get('Value'))

            if prop == 'capacity':
                capacity = num
            elif prop == 'voltage':
                voltage = num
            elif prop in ('coulombic_efficiency', 'coulombic efficiency'):
                coulombic_efficiency = num
            elif prop in ('energy_density', 'energy density'):
                energy_density = num
            elif prop == 'conductivity':
                conductivity = num

            entry = BatteryProperties(
                material_name=row.get('Name'),
                capacity=capacity,
                voltage=voltage,
                coulombic_efficiency=coulombic_efficiency,
                energy_density=energy_density,
                conductivity=conductivity,
                doi=row.get('DOI'),
                journal=row.get('Journal')
            )
            archive.m_add_sub_section(archive.section_run, entry)

    @staticmethod
    def _to_float(value):
        try:
            s = str(value).replace('–', '-')
            match = re.search(r'-?\d+\.?\d*', s)
            return float(match.group()) if match else None
        except Exception:
            return None
