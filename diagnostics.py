import time
from controller import OmronVNCInterface

interface = OmronVNCInterface('menu.yaml')
interface.connect_vnc()

test_err = True
test_cells = True
test_shutters = True
test_gatevalves = True

if test_err:

    print("READING ERR")

    print("vacuum status",interface.read_param(['menu','status','vacuum']))
    print("vacuum_gv status",interface.read_param(['menu','status','vacuum_gv']))
    print("vacuum_dpm_gv status",interface.read_param(['menu','status','vacuum_dpm_gv']))
    print("coolant status",interface.read_param(['menu','status','coolant']))
    print("gv1 status",interface.read_param(['menu','status','gv1']))
    print("gv_dpm status",interface.read_param(['menu','status','gv_dpm']))
    print("power status",interface.read_param(['menu','status','power']))
    print("alarm status",interface.read_param(['menu','status','alarm']))

#######################

if test_cells:

    print("TESTING CELLS")
    cell_fail = False

    def get_all_cell_status():
        outlist = []
        for cell in range(1,11):
            outlist.append(interface.read_param(['shutter','cell'+str(cell),'status']))
        return outlist

    init_cell_status = get_all_cell_status()

    print("cell status:", init_cell_status)

    print("TOGGLING CELLS")

    for cell in range(1,11):
        interface.click_param(['shutter','cell'+str(cell),'set'])
        time.sleep(0.5)

    toggled_cell_status = get_all_cell_status()

    for i in range(len(init_cell_status)):
        if init_cell_status[i] == toggled_cell_status[i]:
            print("ERR: CELL",i+1,"FAILURE")
            cell_fail = True

    for cell in range(1,11):
        interface.click_param(['shutter','cell'+str(cell),'set'])
        time.sleep(0.5)

    final_cell_status = get_all_cell_status()

    for i in range(len(init_cell_status)):
        if init_cell_status[i] != final_cell_status[i]:
            print("ERR: CELL",i+1,"FAILURE")
            cell_fail = True

    if cell_fail:
        print("CELL SHUTTER TEST FAIL")
    else:
        print("CELL SHUTTER TEST PASS")

#######################

if test_shutters:

    print("TESTING ALT SHUTTERS")


    o_inj_init = interface.read_param(['shutter','o_inj','status'])
    interface.click_param(['shutter','o_inj','set'])
    if o_inj_init == interface.read_param(['shutter','o_inj','status']):
        print("O-INJ FAIL")
    interface.click_param(['shutter','o_inj','set'])
    if o_inj_init != interface.read_param(['shutter','o_inj','status']):
        print("O-INJ FAIL")
    else:
        print("O-INJ COMPLETE")

    egun_init = interface.read_param(['shutter','egun1','status'])
    interface.click_param(['shutter','egun1','set'])
    if egun_init == interface.read_param(['shutter','egun1','status']):
        print("EGUN1 FAIL")
    interface.click_param(['shutter','egun1','set'])
    if egun_init != interface.read_param(['shutter','egun1','status']):
        print("EGUN1 FAIL")
    else:
        print("EGUN1 COMPLETE")

    mainshutter_init = interface.read_param(['shutter','mainshutter','status'])
    interface.click_param(['shutter','mainshutter','set'])
    if mainshutter_init == interface.read_param(['shutter','mainshutter','status']):
        print("MAINSHUTTER FAIL")
    interface.click_param(['shutter','mainshutter','set'])
    if mainshutter_init != interface.read_param(['shutter','mainshutter','status']):
        print("MAINSHUTTER FAIL")
    else:
        print("MAINSHUTTER COMPLETE")

#######################

if test_gatevalves:

    print("TESTING GATE VALVES")

    gv1_status = interface.read_param(['gate_valve','gv1','open','status'])
    if gv1_status == False:
        # open then close gate valve
        interface.click_param(['gate_valve','gv1','open','set'])
        time.sleep(3)

        if False == interface.read_param(['gate_valve','gv1','open','status']):
            print("GV1 FAIl")

        interface.click_param(['gate_valve','gv1','close','set'])
        time.sleep(3)

        if True == interface.read_param(['gate_valve','gv1','open','status']):
            print("GV1 FAIl")

        print("GV1 COMPLETE")

    if gv1_status == True:
        # close then open gate valve
        interface.click_param(['gate_valve','gv1','close','set'])
        time.sleep(3)

        if True == interface.read_param(['gate_valve','gv1','open','status']):
            print("GV1 FAIl")

        interface.click_param(['gate_valve','gv1','open','set'])
        time.sleep(3)

        if False == interface.read_param(['gate_valve','gv1','open','status']):
            print("GV1 FAIl")

        print("GV1 COMPLETE")

    gv_dpm_status = interface.read_param(['gate_valve','gv1','open','status'])
    if gv_dpm_status == False:
        # open then close gate valve
        interface.click_param(['gate_valve','gv_dpm','open','set'])
        time.sleep(3)

        if False == interface.read_param(['gate_valve','gv_dpm','open','status']):
            print("GV_DPM FAIl")

        interface.click_param(['gate_valve','gv_dpm','close','set'])
        time.sleep(3)

        if True == interface.read_param(['gate_valve','gv_dpm','open','status']):
            print("GV_DPM FAIl")

        print("GV_DPM COMPLETE")

    if gv_dpm_status == True:
        # close then open gate valve
        interface.click_param(['gate_valve','gv_dpm','close','set'])
        time.sleep(3)

        if True == interface.read_param(['gate_valve','gv_dpm','open','status']):
            print("GV_DPM FAIl")

        interface.click_param(['gate_valve','gv_dpm','open','set'])
        time.sleep(3)

        if False == interface.read_param(['gate_valve','gv_dpm','open','status']):
            print("GV_DPM FAIl")

        print("GV_DPM COMPLETE")
