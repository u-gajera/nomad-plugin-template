# from nomad.config.models.plugins import AppEntryPoint
# from nomad.config.models.ui import App, Column, Columns, FilterMenu, FilterMenus

# app_entry_point = AppEntryPoint(
#     name='NewApp',
#     description='New app entry point configuration.',
#     app=App(
#         label='NewApp',
#         path='app',
#         category='simulation',
#         columns=Columns(
#             selected=['entry_id'],
#             options={
#                 'entry_id': Column(),
#             },
#         ),
#         filter_menus=FilterMenus(
#             options={
#                 'material': FilterMenu(label='Material'),
#             }
#         ),
#     ),
# )

from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App, Column, Menu, MenuItemTerms, MenuItemHistogram, SearchQuantities
)

schema = 'nomad_battery_data.schema_packages.schema_package.m_package#BatteryProperties'

battery_data_app = AppEntryPoint(
    name='BatteryDataApp',
    description='Explore battery material properties.',
    app=App(
        label='Battery Data',
        path='battery-data',
        category='Materials',
        readme="""
            Brrowse and filter Battery Experimental battery materials by capacity, voltage, energy density, 
            See distributions, and drill down by composition.
        """,
        # Make your custom schema available
        search_quantities=SearchQuantities(
            include=[f'*#{schema}']
        ),
        # Which columns show up in the result table by default
        columns=[
            Column(quantity='entry_id',           selected=True),
            Column(quantity=f'data.section_run.capacity#{schema}',           selected=True),
            Column(quantity=f'data.section_run.voltage#{schema}',            selected=True),
            Column(quantity=f'data.section_run.energy_density#{schema}',     selected=True),
            Column(quantity=f'data.section_run.coulombic_efficiency#{schema}', selected=False),
            Column(quantity=f'data.section_run.conductivity#{schema}',       selected=False),
            Column(quantity='upload_create_time',    selected=False),
        ],
        # Always limit to entries parsed by your schema
        filters_locked={
            'section_run.definition_qualified_name': [schema]
        },
        # Sidebar menu: terms filter plus histograms
        menu=Menu(
            title='Filters',
            items=[
                Menu(
                    title='Material Name',
                    items=[
                        MenuItemTerms(quantity=f'data.section_run.material_name#{schema}')
                    ]
                ),
                Menu(
                    title='Properties',
                    items=[
                        MenuItemHistogram(x=f'data.section_run.capacity#{schema}'),
                        MenuItemHistogram(x=f'data.section_run.voltage#{schema}'),
                        MenuItemHistogram(x=f'data.section_run.energy_density#{schema}')
                    ]
                )
            ]
        ),
        # Default dashboard: capacity histogram
        dashboard={
            'widgets': [
                {
                    'type': 'histogram',
                    'quantity': f'data.section_run.capacity#{schema}',
                    'nbins': 25,
                    'autorange': True,
                    'show_input': False,
                    'layout': {
                        'lg': {'x': 0, 'y': 0, 'w': 12, 'h': 4}
                    }
                }
            ]
        }
    )
)
