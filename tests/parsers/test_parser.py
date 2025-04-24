# import logging

# from nomad.datamodel import EntryArchive

# from nomad_battery_data.parsers.parser import NewParser


# def test_parse_file():
#     parser = NewParser()
#     archive = EntryArchive()
#     parser.parse('tests/data/example.out', archive, logging.getLogger())

#     assert archive.workflow2.name == 'test'

import os
import pandas as pd
import pytest

from nomad.datamodel import EntryArchive
from nomad_battery_data.parsers.parser import BatteryDataParser


def test_parse_battery_csv_creates_entries():
    # Path to the sample CSV (placed under tests/data)
    base = os.path.dirname(__file__)
    csv_path = os.path.join(base, '..', 'data', 'test_battery_data.csv')

    parser = BatteryDataParser()
    archive = EntryArchive()
    parser.parse(csv_path, archive, logger=None)

    # Read CSV to compare
    df = pd.read_csv(csv_path)

    # One parsed entry per CSV row
    assert len(archive.section_run) == len(df), \
        f"Expected {len(df)} entries, got {len(archive.section_run)}"


def test_parse_battery_csv_field_mapping():
    base = os.path.dirname(__file__)
    csv_path = os.path.join(base, '..', 'data', 'test_battery_data.csv')

    df = pd.read_csv(csv_path)
    parser = BatteryDataParser()
    archive = EntryArchive()
    parser.parse(csv_path, archive, logger=None)

    # Check first three rows for correct mapping
    for idx in range(min(3, len(df))):
        row = df.iloc[idx]
        entry = archive.section_run[idx]
        # Material name always maps
        assert entry.material_name == row['Name']
        # Determine expected numeric
        try:
            expected = float(str(row['Value']).replace('–','').split()[0])
        except Exception:
            expected = None
        prop = str(row['Property']).strip().lower()
        if prop == 'capacity':
            assert entry.capacity == pytest.approx(expected)
            assert entry.voltage is None
        elif prop == 'voltage':
            assert entry.voltage == pytest.approx(expected)
            assert entry.capacity is None
        # start adding additional property checks similarly

#can be checked using pytest tests/parsers/test_parser.py