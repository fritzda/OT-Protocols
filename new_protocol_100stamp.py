from opentrons import protocol_api

metadata = {
    "protocolName": "180ul stamp to 9 plates",
    "description": "180ul stamp to 9 plate",
    "author": "New API User DAF"
    }
requirements = {"robotType": "Flex", "apiLevel": "2.24"}

def add_parameters(parameters):
    parameters.add_float(
        variable_name="dispense_volume",
        display_name="Volume to dispense (in µL)",
        default=100.0,
        minimum=1.0,
        maximum=1000.0
    )

    parameters.add_int(
        variable_name="number_of_plates",
        display_name="Number of plates to include",
        default=1,
        minimum=1,
        maximum=9  # Adjust depending on how many you support on deck
    )

def run(protocol: protocol_api.ProtocolContext):

    global dispense_volume
    dispense_volume = protocol.params.dispense_volume

    global number_of_plates
    number_of_plates = protocol.params.number_of_plates

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
        


    #You may notice that the value of tip_racks is in brackets, indicating that it’s a list. 
    # This serial dilution protocol only uses one tip rack, but some protocols require more tips, 
    # so you can assign them to a pipette all at once, like tip_racks=[tips1, tips2].

    #Measure out equal amounts of diluent from the reservoir to every well on the plate.
    #Measure out equal amounts of solution from the reservoir into wells in the first column of the plate.
    #Move a portion of the combined liquid from column 1 to 2, then from column 2 to 3, and so on all the way to column 12.


    ##Single Channel Pippete
    # left_pipette.transfer(100, reservoir["A1"], plate.wells()) # For every well on the plate, aspirate 100 µL of fluid from column 
    # #(A)1 of the reservoir and dispense it in the well.

    # for i in range(8):
    #     row = plate.rows()[i]
    #     left_pipette.transfer(100, reservoir["A2"], row[0], mix_after=(3, 50)) #mix 3 times with 50 µL of fluid each time.
    #     #Python lists are zero-indexed, but columns on labware start numbering at 1, 
    #     #this will be well A1 on the first time through the loop, B1 the second time, and so on

    #     left_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50)) # So the source is row[:11], from the beginning of the row until its 11th item. 
    #     #And the destination is row[1:], from index 1 (column 2!) until the end. 


    ##8 Channel Pipette
    # whenever you target a well in row A of a plate with an 8-channel pipette, it will move its topmost tip to row A, lining itself up over the entire column.
    # Thus, when adding the diluent, instead of targeting every well on the plate, you should only target the top row:#


    # pick up tip
    pipette.pick_up_tip()


   # Collect all destination wells (A1 of each plate)
    destinations = [plate["A1"].top() for plate in plates]

    pipette.flow_rate.dispense = 94 # 94ul/second as determined by Leo in Dolan lab

    
    # Distribute 180 µL to each plate’s A1 with 50 µL disposal volume
    pipette.distribute(
        volume= dispense_volume,
        source=reservoir["A1"],
        dest=destinations,
        disposal_volume = 15,
        new_tip= "never",  # use one tip for entire distribute
        blow_out= True,
        touch_tip = True,
        blowout_location= "source well" ,
        keep_last_tip = True
    )

    # Touch off droplets
    pipette.blow_out(reservoir["A1"].bottom(z=1))


    #Drop tip
    pipette.return_tip()
