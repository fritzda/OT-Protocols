from opentrons import protocol_api

metadata = {
    "protocolName": "100ul stamp to 3 plates",
    "description": "100ul stamp to 3 plate",
    "author": "New API User DAF"
    }
requirements = {"robotType": "Flex", "apiLevel": "2.24"}

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware(
        "opentrons_flex_96_filtertiprack_1000ul", location="A1",
        adapter="opentrons_flex_96_tiprack_adapter"
    )
    
    reservoir = protocol.load_labware("nest_1_reservoir_290ml", location="B1")
    
    
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", location="A2")
    plate2 = protocol.load_labware("corning_96_wellplate_360ul_flat", location="B2")
    plate3 = protocol.load_labware("corning_96_wellplate_360ul_flat", location="C2")


    trash = protocol.load_trash_bin("A3")

    #Load Pipettes
    pipette = protocol.load_instrument(
            instrument_name="flex_96channel_1000", tip_racks=[tips]
    )


    
    


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

   # Pick up tips all heads
    pipette.pick_up_tip()

    # Aspirate from Res
    pipette.aspirate(volume=300, location=reservoir["A1"])

    # Dispense to plate in first well. 96 head can only access A1 in all labware
    pipette.dispense(volume=100, location=plate["A1"])

    pipette.dispense(volume=100, location=plate2["A1"])
    
    pipette.dispense(volume=100, location=plate3["A1"])







    pipette.return_tip()