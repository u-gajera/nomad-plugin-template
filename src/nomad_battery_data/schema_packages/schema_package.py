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
# from nomad.datamodel.data import Schema
# from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
# from nomad.metainfo import Quantity, SchemaPackage

# configuration = config.get_plugin_entry_point(
#     'nomad_battery_data.schema_packages:schema_package_entry_point'
# )

# m_package = SchemaPackage()


# class NewSchemaPackage(Schema):
#     name = Quantity(
#         type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
#     )
#     message = Quantity(type=str)

#     def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
#         super().normalize(archive, logger)

#         logger.info('NewSchema.normalize', parameter=configuration.parameter)
#         self.message = f'Hello {self.name}!'


# m_package.__init_metainfo__()

from nomad.datamodel.data import EntryData
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np

m_package = SchemaPackage()

class BatteryProperties(EntryData):
    """
    Schema representing battery material properties from Prof Cole database.
    """

    material_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="Name/Compound of the battery material."
    )

    capacity = Quantity(
        type=np.float64,
        unit='m*A*hour/g',
        description="Battery charge capacity per unit mass(g).",
        default=None
    )

    voltage = Quantity(
        type=np.float64,
        unit='V',
        description="Electrical potential difference (Voltage).",
        default=None
    )

    coulombic_efficiency = Quantity(
        type=np.float64,
        unit='',
        description="Ratio of extracted charge to input charge per cycle.",
        default=None
    )

    energy_density = Quantity(
        type=np.float64,
        unit='W*hour/kg',
        description="Energy stored per unit mass.",
        default=None
    )

    conductivity = Quantity(
        type=np.float64,
        unit='S/m',
        description="Electrical conductivity of battery material.",
        default=None
    )

    doi = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description="DOI for source publication.",
        default=None
    )

    journal = Quantity(
        type=str,
        description="Publishing journal.",
        default=None
    )

m_package.__init_metainfo__()
