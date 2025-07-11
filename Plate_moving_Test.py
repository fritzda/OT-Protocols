from opentrons import protocol_api

metadata = {
    "protocolName": "plate moving test",
    "description": """This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. 
                   It moves a plate around""",
    "author": "DAF"
    }
requirements = {"robotType": "Flex", "apiLevel": "2.20"}



#Moving autmoatic vs manual 


def run(protocol: protocol_api.ProtocolContext):

    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "D1")

    # have the gripper move the plate from D1 to D2
    protocol.move_labware(labware=plate, new_location="D2", use_gripper=True)

    # pause to move the plate manually from D2 to D3
    protocol.move_labware(labware=plate, new_location="D3", use_gripper=False)

    # pause to move the plate manually from D3 to C1
    protocol.move_labware(labware=plate, new_location="C1")
    
    # have the gripper move the plate from C1 to D1
    protocol.move_labware(labware=plate, new_location="D1", use_gripper=True)

    hs_mod = protocol.load_module("heaterShakerModuleV1", "A1")
    # hs_adapter = hs_mod.load_adapter("opentrons_96_flat_bottom_adapter") #Adapter only work with plates 
    # # that don't have a solid bottom like nest

    hs_mod.open_labware_latch()

    protocol.move_labware(
        labware=plate, new_location=hs_mod, use_gripper=True
    )
