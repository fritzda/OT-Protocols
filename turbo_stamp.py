from opentrons import protocol_api

metadata = {
    "protocolName": "Turbo Mode: Customizable plate filling",
    "description": "WARNING: THIS IS RISKY PROTOCOL. The robot will move directly to the next plate. Unless you can guarentee it won't hit anything, don't run this. Customizable volume filling/stamping across n plates",
    "author": "DAF/VEIU"
    }
requirements = {"robotType": "Flex", "apiLevel": "2.24"}

def add_parameters(parameters):
    parameters.add_float(
        variable_name="dispense_volume",
        display_name="Dispense volume",
        description= "Volume (in uls) to dispense into each well.",
        default=100.0,
        minimum=1.0,
        maximum=1000.0
    )

    parameters.add_int(
        variable_name="number_of_plates",
        display_name="Number of plates",
        description = "Number of plates you'd like to fill.",
        default=1,
        minimum=1,
        maximum=9  # Adjust depending on how many you support on deck
    )

    parameters.add_float(
        variable_name="dispense_speed",
        display_name = "Dispense flowrate",
        description ="Flow rate of dispense steps (in ul/sec).",
        default= 94, # 94ul/second as determined by Leo in Dolan lab to protect monolayer
        minimum=1,
        maximum=160  
    )

    parameters.add_float(
        variable_name="aspirate_speed",
        display_name = "Aspirate flowrate",
        description = "Flow rate of aspirate steps (in ul/sec).",
        default= 160,
        minimum=1,
        maximum=160  
    )

    parameters.add_str(
        variable_name="blowout_speed_mode",
        display_name="Blowout speed mode",
        description="Use dispense speed or custom value for blowout.",
        default="match_dispense",
        choices=[
            {"display_name": "Match dispense speed", "value": "match_dispense"},
            {"display_name": "Set manually", "value": "manual"}
        ]
    )

    parameters.add_float(
        variable_name="blowout_speed",
        display_name="Manual blowout flowrate",
        description="Used only if blowout speed mode is set to 'manual'.",
        default=94.0,
        minimum=1,
        maximum=160
    )

def run(protocol: protocol_api.ProtocolContext):

# Set based on runtime params
    dispense_volume = protocol.params.dispense_volume
    number_of_plates = protocol.params.number_of_plates
    dispense_speed = protocol.params.dispense_speed
    aspirate_speed = protocol.params.aspirate_speed
    blowout_speed_mode = protocol.params.blowout_speed_mode
    manual_blowout_speed = protocol.params.blowout_speed

    tips = protocol.load_labware(
        "opentrons_flex_96_filtertiprack_1000ul", location="A1",
        adapter="opentrons_flex_96_tiprack_adapter"
    )
    
    reservoir = protocol.load_labware("nest_1_reservoir_290ml", location="B1")
    
    
    # Define up to 9 locations for 96-well plates, in snake fashion
    plate_locations = ["A2", "B2", "B3", "C3", "C2", "C1", "D1", "D2", "D3"]

    # Load plates dynamically
    plates = [
        protocol.load_labware("corning_96_wellplate_360ul_flat", loc)
        for loc in plate_locations[:number_of_plates]  # <-- Change to up to 9 as needed
    ]

    trash = protocol.load_trash_bin("A3")

    #Load Pipettes
    pipette = protocol.load_instrument(
            instrument_name="flex_96channel_1000", tip_racks=[tips]
    )


    # Monkey patch of touch tip global defaults 
    # Immediately after loading pipette
    # Override default touch_tip parameters globally for pipette

    
    def custom_touch_tip(self, location=None, **kwargs):
        kwargs["radius"] = 0.85
        kwargs["v_offset"] = -1.0
        kwargs["speed"] = 15
        return self.__class__.touch_tip(self, location=location, **kwargs)

    pipette.touch_tip = custom_touch_tip.__get__(pipette)
        

    
    # pick up tip
    pipette.pick_up_tip()


  


   # Collect all destination wells (A1 of each plate)
    destinations = [plate["A1"].top() for plate in plates]


    pipette.flow_rate.dispense = dispense_speed
    
    pipette.flow_rate.aspirate = aspirate_speed

    disposal_volume = dispense_volume * 0.05

    if blowout_speed_mode == "manual":
        blowout_speed = manual_blowout_speed
    else:
        blowout_speed = dispense_speed


    



   

    from opentrons.types import Location

    # Aspirate once for all dispenses (volume × number of plates + disposal)
    pipette.aspirate(
        volume=dispense_volume * number_of_plates + disposal_volume,
        location=reservoir["A1"],
        flow_rate=aspirate_speed
    )


    # Dispense into each plate
    for i, dest_plate in enumerate(plates):
        well = dest_plate["A1"]
        depth = well.depth

        # Calculate position 1 mm below the top and 80% to the left
        well_top_left_point = well.from_center_cartesian(
            x=-0.8,
            y=0.0,
            z=1.0 - (1 / depth)
        )
        well_top_left_location = Location(well_top_left_point, well)

        # Move to 10 mm above well (only for force_direct movements)
        if i == 0:
            # First plate: move normally to clear the reservoir
            pipette.move_to(well.top(z=10))
        else:
            # Remaining plates: direct path between wells
            pipette.move_to(well.top(z=10), force_direct=True)

        # Dispense
        pipette.dispense(
            volume=dispense_volume,
            location=well_top_left_location,
            flow_rate=dispense_speed
        )

        pipette.move_to(well.top(z=10))

        pipette.touch_tip()