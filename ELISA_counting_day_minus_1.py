from opentrons import protocol_api
from opentrons.protocol_api import COLUMN, ALL



metadata = {
    'protocolName': 'ELISA Plate Coating Protocol with Shaking',
    'author': 'Assistant',
    'description': 'Protocol to coat plates with buffer using single column tips and heater-shaker mixing with reservoir tracking'
}

##Edit this here for num of plates
num_plates = int(3) 

requirements = {
    "robotType": "Flex", 
    "apiLevel": "2.23"
}

def get_plate_slots(num_plates):
    """Helper function to return plate slots based on number of plates"""
    all_slots = ['C1', 'C2', 'C3', 'D1', 'D2', 'D3']
    if num_plates < 1 or num_plates > 6:
        raise ValueError("Number of plates must be between 1 and 6")
    return all_slots[:num_plates]

def run(protocol: protocol_api.ProtocolContext):
    # Get number of plates from user
    
    # Calculate required volumes and wells
    VOLUME_PER_PLATE = 5000  # 5mL = 5000µL per plate
    VOLUME_PER_WELL = 50  # 50µL per well
    DISPOSAL_VOLUME = 30  # Disposal volume per plate
    RESERVOIR_WELL_CAPACITY = 15000  # 15mL = 15000µL per reservoir well
    
    total_volume_needed = num_plates * (VOLUME_PER_PLATE + DISPOSAL_VOLUME)
  
    num_reservoir_wells_needed = -(-total_volume_needed // RESERVOIR_WELL_CAPACITY)  # Ceiling division
    

    protocol.comment(f"Total volume needed: {total_volume_needed}µL")
    protocol.comment(f"Number of reservoir wells needed: {num_reservoir_wells_needed}")
    
    # Get plate slots based on number of plates
    plate_slots = get_plate_slots(num_plates)
    plate_positions = ", ".join(plate_slots)
    protocol.comment(f"Please place {num_plates} plates in the following positions: {plate_positions}")
    protocol.comment(f"Please fill {num_reservoir_wells_needed} reservoir wells (starting from A1) with <11mL (2 plates) coating solution each")
    
    # Load modules
    heater_shaker = protocol.load_module('heaterShakerModuleV1', 'A1')
    
    # Load trash bin
    trash = protocol.load_trash_bin('A3')

    # Load labware
    plates = [
        protocol.load_labware('corning_96_wellplate_360ul_flat', slot)
        for slot in plate_slots
    ]
    
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'B1')
    
    tiprack_1000 = protocol.load_labware(
        'opentrons_flex_96_filtertiprack_1000ul', 
        'A2',
    )
    tiprack_200 = protocol.load_labware(
        'opentrons_flex_96_filtertiprack_200ul',
        'B2',
    )





    # Load pipette
    pipette = protocol.load_instrument(
        'flex_96channel_1000',
        'left',
        tip_racks=[tiprack_1000, tiprack_200]
    )
    pipette.configure_nozzle_layout(
        style=COLUMN,
        start="A12"
    )

    # Track reservoir well usage
    current_reservoir_well_idx = 0
    volume_remaining_in_well = RESERVOIR_WELL_CAPACITY
    reservoir_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12']

    # Open latch before plate movement
    heater_shaker.open_labware_latch()

    # Protocol steps
    for i, plate in enumerate(plates):
        # Check if we need to switch to next reservoir well
        if volume_remaining_in_well < (VOLUME_PER_PLATE + DISPOSAL_VOLUME):
            current_reservoir_well_idx += 1
            volume_remaining_in_well = RESERVOIR_WELL_CAPACITY
            protocol.comment(f"Switching to reservoir well {reservoir_wells[current_reservoir_well_idx]}")

        # Pick up tips from the corresponding column
      
        pipette.pick_up_tip(tiprack_200.columns()[i][0])
        
        # Transfer coating solution from current reservoir well to plate
        pipette.distribute(
            VOLUME_PER_WELL,
            reservoir[reservoir_wells[current_reservoir_well_idx]],
            [col for col in plate.rows()[0]],
            disposal_vol=DISPOSAL_VOLUME,
            touch_tip=(True,30),
            new_tip='never'   
        )

       # pipette.touch_tip(speed=30)

        # Update remaining volume
        volume_remaining_in_well -= (VOLUME_PER_PLATE + DISPOSAL_VOLUME)
        
        # Move plate to heater-shaker
        protocol.move_labware(
            plate,
            heater_shaker,
            use_gripper=True
        )
        
        # Close latch after placing plate
        heater_shaker.close_labware_latch()

        # Shake plate
        heater_shaker.set_and_wait_for_shake_speed(rpm=200)
        protocol.delay(seconds=30)
        heater_shaker.deactivate_shaker()
        
        # Open latch before removing plate
        heater_shaker.open_labware_latch()
        
        # Move the plate back to its original slot
        protocol.move_labware(
            heater_shaker.labware,
            plate_slots[i],
            use_gripper=True
        )
        
        pipette.drop_tip()

    protocol.comment('Protocol complete. Your Plates are Coated. Please proceed with plate incubation.')

