from opentrons import protocol_api
from opentrons.protocol_api import COLUMN, ALL




metadata = {
    'protocolName': 'ELISA Plate Coating Protocol with Shaking',
    'author': 'Assistant',
    'description': 'Protocol to coat plates with buffer using single column tips and heater-shaker mixing with reservoir tracking'
}

requirements = {
    "robotType": "Flex", 
    "apiLevel": "2.19"
}

z_height_corning = 14.22
z_height_default = {'x':0,'y':0,'z': 2}
lid_offset = {'x':0,'y':0,'z': 2}
lid_offset_drop = {'x':0,'y':0,'z': 2.6}

def run(protocol: protocol_api.ProtocolContext):
  
    pipette = protocol.load_instrument(
        'flex_96channel_1000',
        'left'
        )
    
    pipette.default_speed = 100 #300 is default

    temp_plate_source = protocol.load_labware(
            "corning_96_wellplate_360ul_flat", location="D4"
        )   
    pickup_offset_for_plate_2 = {'x':0,'y':0,'z': z_height_corning-1.5}
    dropoff_offset_for_plate_2 = {'x':0,'y':0,'z': z_height_corning+1.2}
    
    protocol.move_labware(temp_plate_source, "D2", use_gripper=True, pick_up_offset=pickup_offset_for_plate_2, drop_offset = z_height_default)
    
    ### plate now on D2

    ## Remove lid

    protocol.move_labware(temp_plate_source, "D3", use_gripper=True, pick_up_offset=lid_offset, drop_offset = z_height_default)
    del protocol.deck["D3"]
    temp_plate_source = protocol.load_labware(
    "corning_96_wellplate_360ul_flat", location="D2"
    )   
    # Do pipetting Actions here


    # Delete plate and reload lid
    del protocol.deck["D2"]
    temp_plate_source = protocol.load_labware(
    "corning_96_wellplate_360ul_flat", location="D3"
    )   
    # Put lid back on labware
    protocol.move_labware(temp_plate_source, "D2", use_gripper=True, pick_up_offset=z_height_default, drop_offset = lid_offset_drop)
    
    # Put labware into "done" stack
    protocol.move_labware(temp_plate_source, "C4", use_gripper=True, pick_up_offset=z_height_default, drop_offset = z_height_default)
    del protocol.deck["C4"]

    # Move next plate to pip loc


    temp_plate_source = protocol.load_labware(
    "corning_96_wellplate_360ul_flat", location="D4"
    )   
    protocol.move_labware(temp_plate_source, "D2", use_gripper=True, pick_up_offset=z_height_default, drop_offset = z_height_default)
    
    ### plate 2 now on D2 #####################3

    ## Remove lid

    protocol.move_labware(temp_plate_source, "D3", use_gripper=True, pick_up_offset=lid_offset, drop_offset = z_height_default)
    del protocol.deck["D3"]
    temp_plate_source = protocol.load_labware(
    "corning_96_wellplate_360ul_flat", location="D2"
    )   
    # Do pipetting Actions here
    

    # Delete plate and reload lid
    del protocol.deck["D2"]
    temp_plate_source = protocol.load_labware(
    "corning_96_wellplate_360ul_flat", location="D3"
    )   
    # Put lid back on labware
    protocol.move_labware(temp_plate_source, "D2", use_gripper=True, pick_up_offset=z_height_default, drop_offset = lid_offset_drop)
    
    # Put labware into "done" stack
    protocol.move_labware(temp_plate_source, "C4", use_gripper=True, pick_up_offset=z_height_default, drop_offset = dropoff_offset_for_plate_2)
    

    ## Purely curious, can we move the stack alltogether?
    protocol.move_labware(temp_plate_source, "D4", use_gripper=True, pick_up_offset=z_height_default, drop_offset = z_height_default)
    ##A:  Yes we can :)))