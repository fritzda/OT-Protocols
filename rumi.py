# flake8: noqa
from opentrons import protocol_api
import math
from opentrons.protocol_api import COLUMN, ALL

metadata = {
    'ctx.Name': 'Stamping Protocol',
    'author': 'Rami Farawi <ndiehl@opentrons.com',
}
requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.19'
}

def add_parameters(parameters):

    parameters.add_bool(
    variable_name="real_mode",
    display_name="Real Mode",
    description="When on real incubation times",
    default=True
)

def run(ctx: protocol_api.ProtocolContext):

    real_mode = ctx.params.real_mode

    # DECK LABWARE
    reservoir_one = [ctx.load_labware('nest_1_reservoir_290ml', slot) for slot in ['D1', 'D2']]
    pbs = reservoir_one[0]['A1']
    # primary_antibody = reservoir_one[1]['A1']
    waste = reservoir_one[1]['A1']

    reservoir_12 = ctx.load_labware('nest_12_reservoir_15ml', 'C1')
    nds = reservoir_12['A1']
    primary_antibody = reservoir_12['A2']

    trash = ctx.load_waste_chute()

    plate_96 = ctx.load_labware('corning_96_wellplate_360ul_flat', 'C2')


    tiprack_adapters = [ctx.load_adapter('opentrons_flex_96_tiprack_adapter', slot) for slot in ['B3']]
    tiprack200 = [tiprack_adapters[0].load_labware('opentrons_flex_96_tiprack_200ul')]
    tiprack1000 = ctx.load_labware('opentrons_flex_96_tiprack_1000ul', 'B1')

    # LOAD PIPETTES
    p = ctx.load_instrument("flex_96channel_1000")



    def pick_up(tiprack):
        if tiprack == 'full':


            p.configure_nozzle_layout(
                style=ALL,
                tip_racks=tiprack200
            )

            p.reset_tipracks()
            p.pick_up_tip()

        else:

            p.configure_nozzle_layout(
                style=COLUMN,
                start="A1",
                tip_racks=[tiprack1000]
            )
            p.pick_up_tip()

    cell_well = plate_96['A1']


    # add pbs
    pick_up('full')
    for _ in range(3):
        p.aspirate(100, pbs)
        p.dispense(100, cell_well)
        p.aspirate(100, cell_well)
        p.dispense(100, waste)
    p.return_tip()

    # add nds
    pick_up('partial')
    p.distribute(100, nds, [col for col in plate_96.rows()[0]], new_tip='never')
    p.drop_tip()

    ctx.delay(minutes=30 if real_mode else 1)

    # pick off nds
    pick_up('full')
    p.aspirate(100, cell_well)
    p.dispense(100, waste)
    p.return_tip()

    # add primary antibody
    pick_up('partial')
    p.distribute(80, primary_antibody, [col for col in plate_96.rows()[0]], new_tip='never')
    p.drop_tip()

    ctx.delay(minutes=90 if real_mode else 1)

    pick_up('full')
    for i in range(3):
        p.aspirate(100, pbs)
        p.dispense(100, cell_well)
        p.aspirate(180 if i == 0 else 100, cell_well)
        p.dispense(180 if i == 0 else 100, waste)
    p.return_tip()

    # loading liquids

    # Assigning Liquid and colors - this is for the opentrons app display
    pbs_liq = ctx.define_liquid(
    name="PBS",
    description="PBS",
    display_color="#7EFF42",
    )
    secondary_antibody_liq = ctx.define_liquid(
    name="Secondary Antibody",
    description="Secondary Antibody",
    display_color="#50D5FF",
    )
    primary_antibody_liq = ctx.define_liquid(
    name="Primary Antibody",
    description="Primary Antibody",
    display_color="#B925FF",
    )
    cells = ctx.define_liquid(
    name="Cells",
    description="Cells",
    display_color="#B925FF",
    )


    primary_antibody.load_liquid(liquid=primary_antibody_liq, volume=10000)
    nds.load_liquid(liquid=secondary_antibody_liq, volume=10000)
    pbs.load_liquid(liquid=pbs_liq, volume=10000)

    for well in plate_96.wells():
        well.load_liquid(liquid=cells, volume=100)
