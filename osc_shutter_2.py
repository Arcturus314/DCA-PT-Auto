import time
from controller import OmronVNCInterface

interface = OmronVNCInterface('menu.yaml')
interface.connect_vnc()

test_err = True
test_cells = True
toggle_shutter2 = True

period = 10 # seconds

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

    print("CHECKING CELL STATUS")

    def get_all_cell_status():
        outlist = []
        for cell in range(1,11):
            outlist.append(interface.read_param(['shutter','cell'+str(cell),'status']))
        return outlist

    init_cell_status = get_all_cell_status()
    print("cell status:", init_cell_status)

#######################

if toggle_shutter2:

    print("TOGGLING SHUTTER 2")

    while True:

        print("ON")
        interface.click_param(['shutter','cell2','set'])
        time.sleep(period/2)

        print("OFF")
        interface.click_param(['shutter','cell2','set'])
        time.sleep(period/2)

print("DONE")

