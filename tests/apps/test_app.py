# def test_importing_app():
#     # this will raise an exception if pydantic model validation fails for th app
#     from nomad_battery_data.apps import app_entry_point

#     assert app_entry_point.app.label == 'NewApp'
from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App, Column, SearchQuantities,
    Menu, MenuItemTerms, MenuItemHistogram
)

# Fully qualified schema identifier for BatteryProperties
schema = 'nomad_battery_data.schema_packages.schema_package.m_package#BatteryProperties'

battery_data_app = AppEntryPoint(
    name='battery_data_app',
    description='App for browsing battery material property data.',
    app=App(
        label='Battery Data',
        path='battery-data',
        category='materials',
        readme='"""Browse and filter battery materials by capacity, voltage, energy density, and more."""',
        # Make your custom schema available in search
        search_quantities=SearchQuantities(
            include=[f'*#{schema}']
        ),
        # Define which columns to display in the results table
        columns=[
            Column(quantity='entry_id', selected=False),
            Column(quantity=f'data.section_run.material_name#{schema}', selected=True, label='Material'),
            Column(quantity=f'data.section_run.capacity#{schema}', selected=True, label='Capacity (mAh/g)'),
            Column(quantity=f'data.section_run.voltage#{schema}', selected=True, label='Voltage (V)'),
            Column(quantity=f'data.section_run.energy_density#{schema}', selected=True, label='Energy Density (Wh/kg)'),
            Column(quantity=f'data.section_run.coulombic_efficiency#{schema}', selected=False, label='Coulombic Efficiency'),
            Column(quantity=f'data.section_run.conductivity#{schema}', selected=False, label='Conductivity (S/m)'),
            Column(quantity=f'data.section_run.doi#{schema}', selected=False, label='DOI'),
            Column(quantity=f'data.section_run.journal#{schema}', selected=False, label='Journal')
        ],
        # Always restrict queries to entries using your schema
        filters_locked={
            'section_run.definition_qualified_name': [schema]
        },
        # Sidebar filter menus
        menu=Menu(
            title='Filters',
            items=[
                Menu(
                    title='Material Name',
                    items=[
                        MenuItemTerms(
                            quantity=f'data.section_run.material_name#{schema}'
                        )
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
        # Default dashboard widgets
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


    #checking via pytest tests/apps/test_app.py