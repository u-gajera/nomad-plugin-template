# import os.path

# from nomad.client import normalize_all, parse


# def test_schema_package():
#     test_file = os.path.join('tests', 'data', 'test.archive.yaml')
#     entry_archive = parse(test_file)[0]
#     normalize_all(entry_archive)

#     assert entry_archive.data.message == 'Hello Markus!'

import pytest
from nomad_battery_data.schema_packages.schema_package import m_package, BatteryProperties

def test_schema_registration():
    # Ensure the schema package includes the BatteryProperties section
    section_names = [definition.name for definition in m_package.m_definitions]
    assert 'BatteryProperties' in section_names, \
        f"Expected 'BatteryProperties' in schema package, got {section_names}"  

@pytest.mark.parametrize('field', [
    'material_name',
    'capacity',
    'voltage',
    'coulombic_efficiency',
    'energy_density',
    'conductivity',
    'doi',
    'journal',
])
def test_battery_properties_defaults(field):
    # Instantiating without args: every quantity should default to None
    bp = BatteryProperties()
    value = getattr(bp, field)
    assert value is None, f"Field '{field}' defaulted to {value}, expected None"

# can be checked using pytest tests/schema_packages/test_schema_package.py