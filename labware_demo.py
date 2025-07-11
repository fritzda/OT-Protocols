from opentrons import protocol_api

metadata = {
    "protocolName": "labware situation",
    "description": """This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.""",
    "author": "New API User DAF"
    }
requirements = {"robotType": "Flex", "apiLevel": "2.20"}

# def run(protocol: protocol_api.ProtocolContext):
#     #Moving Labware
#     plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "D1")
#     protocol.move_labware(labware=plate, new_location="D2")
#     #When the move step is complete, the API updates the labware’s location, 
#     #so you can move the plate multiple times:
#     protocol.move_labware(labware=plate, new_location="D3")
#     protocol.move_labware(labware=plate, new_location="A2")

#Moving autmoatic vs manual 
def run(protocol: protocol_api.ProtocolContext):
    # For corning plates, the gripper will olny remove the lid if you leave it on. Could be useful 

    plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "D1")

    # have the gripper move the plate from D1 to D2
    protocol.move_labware(labware=plate, new_location="D2", use_gripper=True)

    # pause to move the plate manually from D2 to D3
    protocol.move_labware(labware=plate, new_location="D3", use_gripper=False)

    # pause to move the plate manually from D3 to C1
    protocol.move_labware(labware=plate, new_location="C1")
    
    # have the gripper move the plate from C1 to D1
    protocol.move_labware(labware=plate, new_location="D1", use_gripper=True)


# def run(protocol: protocol_api.ProtocolContext):
#     tiprack = protocol.load_labware(
#         load_name = "opentrons_flex_96_tiprack_200ul", 
#         location= "D1",
#         label= "p200 tips")
#     reservoir = protocol.load_labware(
#         load_name = "nest_12_reservoir_15ml", 
#         location ="D3")
#     plate = protocol.load_labware(
#         load_name= "corning_96_wellplate_360ul_flat", 
#         location= "D2",
#         label= "corning 96w flat bottom")

#     depth = plate["A1"].depth  # 10.67
#     # print(depth)
   
#     # hs_mod = protocol.load_module(
#     #     module_name= "heaterShakerModuleV1", 
#     #     location= "C1")
#     # hs_adapter = hs_mod.load_adapter(
#     #     name= "opentrons_96_flat_bottom_adapter")
#     # hs_plate = hs_adapter.load_labware(
#     #     name="nest_96_wellplate_200ul_flat")
    
#     trash = protocol.load_trash_bin(
#         location="A3")
#     left_pipette = protocol.load_instrument("flex_8channel_1000", "left", tip_racks=[tiprack])

#     # a1 = plate.wells_by_name()["A1"]
#     # d6 = plate["D6"]  # dictionary indexing
    
#     # for well in plate.rows()[0]:
#     #     left_pipette.transfer(reservoir["A1"], well, 50)

#     # #Defining Liquids
#     # greenWater = protocol.define_liquid(
#     # name="Green water",
#     # description="Green colored water for demo",
#     # display_color="#00FF00",
#     # )
    
#     # blueWater = protocol.define_liquid(
#     # name="Blue water",
#     # description="Blue colored water for demo",
#     # display_color="#0000FF",
#     # )
#     # well_plate["A1"].load_liquid(liquid=greenWater, volume=50)
#     # well_plate["A2"].load_liquid(liquid=greenWater, volume=50)
#     # well_plate["B1"].load_liquid(liquid=blueWater, volume=50)
#     # well_plate["B2"].load_liquid(liquid=blueWater, volume=50)
#     # reservoir["A1"].load_liquid(liquid=greenWater, volume=200)
#     # reservoir["A2"].load_liquid(liquid=blueWater, volume=200)


