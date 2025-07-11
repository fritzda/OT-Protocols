# Version 1 - August 21, 2024


from opentrons import protocol_api
from opentrons.protocol_api import COLUMN, ALL
from opentrons import types
# points syntax
#p96.aspirate(100, well.bottom(2).move(types.Point(x=-2, y=2, z =-1)))
import math

metadata = {
    'protocolName': 'Demo Protocol to test Partial Column Pickup of Tiprack using A1 and A12 row of pipette',
    'author': 'Anurag Kanase',
    'description': 'This protocol enables to test partial column tip pickup for 96-ch pipette. The protocol is intended to verify Column tip pickup is functional and working '
}
requirements = {"robotType": "Flex", "apiLevel": "2.19"}

def add_parameters(parameters: protocol_api.Parameters): 

    parameters.add_int(
        variable_name="tiprack",
        display_name="Select Tiprack",
        description="Select tiprack for 96-ch partial pickup test",
        default=0,
        choices=[
            {"display_name": "50 µL tiprack", "value": 0},
            {"display_name": "200 µL tiprack", "value": 1},
            {"display_name": "1000 µL tiprack", "value": 2},
        ]
    )

    parameters.add_int(
        display_name="How many columns?",
        variable_name="columns",
        default=3,minimum=1,maximum=6,
        description="Select total columns to pickup from tiprack. \nNote: columns x 16 tips will be trashed")

    parameters.add_int(
        variable_name="waste",
        display_name="Select Waste Bin Type",
        description="Is your deck setup with trashbin or chute?",
        default=0,
        choices=[
            {"display_name": "Waste Chute", "value": 0},
            {"display_name": "Trash Bin", "value": 1},
        ]
    )
def run(protocol: protocol_api.ProtocolContext):

    tiprack = ["opentrons_flex_96_filtertiprack_50ul",
               "opentrons_flex_96_filtertiprack_200ul",
               "opentrons_flex_96_filtertiprack_1000ul"][protocol.params.tiprack]
    
    rack = tiprack.split("_")[-1]


    protocol.pause("Before we begin, let's make sure we have the following:")
    protocol.pause(f"Do you have ** {rack} ** tiprack placed on C2?")
    protocol.pause("Note: Tips will be discarded in the waste chute.\nCan you attach something to grab the clean tips?")

    tips = protocol.load_labware(tiprack, "C2", label = rack)
    p96 = protocol.load_instrument('flex_96channel_1000', 'left')
    if protocol.params.waste == 0:
        trash = protocol.load_waste_chute()
    else:
        trash = protocol.load_trash_bin("A3")

    protocol.comment("----> Picking up tips from Column 12 to left")
    for start_loc in ["A1", "A12"]:
        
        
        p96.configure_nozzle_layout(
            style=COLUMN,
            start=start_loc,
            tip_racks=[tips]) 
        
        for i in range(protocol.params.columns):
            p96.pick_up_tip()
            p96.home()
            protocol.delay(5)
            p96.drop_tip()
        protocol.comment("---- > Picking up tips from Column 1 to right")
    