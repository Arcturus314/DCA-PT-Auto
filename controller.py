from vncdotool import api
from PIL import Image
import yaml
import os

def print_dict(dict_in):
    print_dict_worker(dict_in, 0)

def print_dict_worker(inel, hierarchy_level):
    if type(inel) != dict: # base case
        print(" "*hierarchy_level + str(inel))
        return
    for key in inel:
        print(" "*hierarchy_level + str(key))
        print_dict_worker(inel[key], hierarchy_level+1)

def import_yaml_dict(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc

def compare_against_threshold(rgba):
    print(rgba)
    return False

class OmronVNCInterface:

    # expect a hierarchy of YAML files: all top-level entries in menu.yaml point to other files

    def __init__(self, menu_filename, yaml_path = "templates"):
        # builds YAML configuration file hierarchy

        self.menu_yaml = import_yaml_dict(os.path.join(yaml_path, menu_filename))

        self.screens_yaml = {}

        self.screenshot_filename = "tmp.png"

        for key in self.menu_yaml['screen'].keys():
            yaml_filename = os.path.join(yaml_path, key + ".yaml")
            if not os.path.exists(yaml_filename): continue
            print("--> loading YAML " + yaml_filename)

            self.screens_yaml[key] = import_yaml_dict(yaml_filename)

    def connect_vnc(self, address="10.19.5.16", password="888888"):
        # note: user and pass listed here are defaults in DCA configuration
        self.client = api.connect(address, password=password)
        client.timeout = 2

    def vnc_click_location(self, x, y):
        # need some error catching here
        while (1):
            try:
                self.client.mouseMove(x, y)
                self.client.mousePress(1)
                return
            except TimeoutError:
                print("Communication error with VNC server...")


    def vnc_read_location(self, x, y):
        # this is a bad solution. Takes screenshot, then returns pixel location at specific coordinates.

        # fetching screenshot
        client.captureScreen(self.screenshot_filename)

        # processing screenshot
        im = Image.open(self.screenshot_filename)
        pix = im.load()
        rgba = pix[x, y]

        return rgba

    def print_hierarchy(self):
        print("----TOP MENU----")
        print_dict(self.menu_yaml)

        print("----SCREENS----")
        print_dict(self.screens_yaml)

    def fetch_leaf_dict(path, indict):
        if len(path) == 1:
            return indict[path[0]]
        if type(indict) != dict:
            return indict
        else:
            fetch_leaf_dict(path[1:], indict[path[0]])


    def click_param(self, path):
        # sets specific parameter. Navigates to correct screen through menu, then clicks on parameter in screen
        # expects path formatted as ['base', 'entry 1', ...]

        if path[0] == 'menu':
            # these are available on any screen, so don't need to change screens prior
            coords = fetch_leaf_dict(path, self.menu_yaml)
            if 'x' not in coords.keys():
                raise RuntimeError("path does not fully specify object",path)
            x_coord = coords['x']
            y_coord = coords['y']

            vnc_click_location(x_coord, y_coord)

        else:
            # need to switch to the specified screen prior to clicking the desired button

            click_param(['menu','screen',path[0]])
            coords = fetch_leaf_dict(path, self.screens_yaml)
            if 'x' not in coords.keys():
                raise RuntimeError("path does not fully specify object",path)
            x_coord = coords['x']
            y_coord = coords['y']

            vnc_click_location(x_coord, y_coord)

    def read_param(path):
        # reads specific parameter. Navicates to correct screen through menu, then reads pixel value of parameter and compares to threshold
        # expects path formatted as ['base', 'entry 1', ...]

        if path[0] == 'menu':
            # these are available on any screen, so don't need to change screens prior
            coords = fetch_leaf_dict(path, self.menu_yaml)
            if 'x' not in coords.keys():
                raise RuntimeError("path does not fully specify object",path)
            x_coord = coords['x']
            y_coord = coords['y']

            rgba = vnc_read_location(x_coord, y_coord)

            return compare_against_threshold(rgba)

        else:
            # need to switch to the specified screen prior to clicking the desired button

            click_param(['menu','screen',path[0]])
            coords = fetch_leaf_dict(path, self.screens_yaml)
            if 'x' not in coords.keys():
                raise RuntimeError("path does not fully specify object",path)
            x_coord = coords['x']
            y_coord = coords['y']

            rgba = vnc_read_location(x_coord, y_coord)

            return compare_against_threshold(rgba)


interface = OmronVNCInterface("menu.yaml")
interface.print_hierarchy()
