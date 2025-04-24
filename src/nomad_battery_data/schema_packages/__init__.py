# from nomad.config.models.plugins import SchemaPackageEntryPoint
# from pydantic import Field


# class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')

#     def load(self):
#         from nomad_battery_data.schema_packages.schema_package import m_package

#         return m_package


# schema_package_entry_point = NewSchemaPackageEntryPoint(
#     name='NewSchemaPackage',
#     description='New schema package entry point configuration.',
# )

from nomad.config.models.plugins import SchemaPackageEntryPoint
from .schema_package import m_package

# Create the entry point that NOMAD will use to discover your schema
battery_data_schema = SchemaPackageEntryPoint(
    name='battery_data_schema',
    description='Schema package for battery material data.',
    package=m_package
)
