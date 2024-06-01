import subprocess
import os
from os import path
import shutil
import stat
import re
import json
import platform

ESC_FILES = [
    "TAESC.gp3",
    "TXESC.ufo",
    "T2ESC.ufo",
    "T3ESC.ufo",
    "T4ESC1.ufo",
    "T4ESC2.ufo"
]
ESC_GIT_REPO = "https://git.taforever.com/ta-forever/taesc.git"
ESC_GIT_DIR = "./taesc/"
EXTRACT_DIR = "./out/"
EXTRACT_WEAPONS_DIR = "./out/weaponE/"
EXTRACT_UNITS_DIR = "./out/unitsE/"
EXTRACT_UNIT_PICS_DIR = "./out/unitpicE/"
EXTRACT_GUIS_DIR = "./out/guiE/"
UNIT_PICS_DIR = "./data/unit_icons/"
UNIT_DATA_PATH = "./data/units.json"
WEAPON_DATA_PATH = "./data/weapons.json"
GUIS_DATA_PATH = "./data/guis.json"

CLASS_REGEX = re.compile(r"\[(\w+)\]")
DATA_REGEX = re.compile(r"(\w*)=([^;]*);")
UNIT_DATA_EXCLUDE_KEYS = {
    "copyright", "version", "corpse"
}
UNIT_DATA_LIST_KEYS = {
    "category", "yardmap"
}
WEAPON_DATA_EXCLUDE_KEYS = {
    "soundstart", "soundhit"
}
WEAPON_DATA_LIST_KEYS = {}
EXCLUDE_UNITS = {
    "GOKT3SUPRPOD"
}
EXCLUDE_WEAPONS = {}
UNIT_DATA = {}
WEAPON_DATA = {}
GUI_DATA = {}


def run_hpi_extract(output_folder, input_file):
    if platform.system().lower() == "windows":
        subprocess.run(["./hpiextract.exe", output_folder, input_file], stdout=subprocess.DEVNULL)
    else:
        subprocess.run(["hpiextract", output_folder, input_file], stdout=subprocess.DEVNULL)


def change_extension(file_path, new_extension):
    return ".".join(file_path.split(".")[:-1]) + "." + new_extension


def fbi_data(file_path):
    data = {}
    
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            
            if line.startswith("//"):
                continue
            
            match = DATA_REGEX.match(line)
            if match:
                key = match.group(1).lower()
                value = match.group(2)
                
                if key in UNIT_DATA_EXCLUDE_KEYS:
                    continue
                
                if key in UNIT_DATA_LIST_KEYS:
                    data[key] = value.strip().split()
                    continue
                
                try:
                    data[key] = int(value)
                except:
                    try:
                        data[key] = float(value)
                    except:
                        data[key] = value
    
    return data


def tdf_data(file_path):
    data = {}
    
    with open(file_path, "r") as f:
        current_weapon = None
        level = 0
        
        for line in f.readlines():
            line = line.strip()
            
            if line.startswith("//"):
                continue
            
            if line == "{":
                level += 1
                continue
            
            if line == "}":
                level -= 1
                continue
            
            match = CLASS_REGEX.match(line)
            if match and match.group(1) != "DAMAGE":
                current_weapon = match.group(1)
                data[current_weapon] = {}
                data[current_weapon]["damage"] = {}
                continue
            
            match = DATA_REGEX.match(line)
            if match:
                key = match.group(1)
                value = match.group(2)
                
                if key in WEAPON_DATA_EXCLUDE_KEYS:
                    continue
                
                if level == 1:
                    placement = data[current_weapon]
                    key = key.lower()
                if level == 2:
                    placement = data[current_weapon]["damage"]
                
                if key in WEAPON_DATA_LIST_KEYS:
                    placement[key] = value.strip().split()
                    continue
                
                try:
                    placement[key] = int(value)
                except:
                    try:
                        placement[key] = float(value)
                    except:
                        placement[key] = value
    
    return data


def gui_data(file_path):
    data = []
    
    with open(file_path, "r") as f:
        level = 0
        current_name = None
        
        for line in f.readlines():
            line = line.strip()
            
            if line.startswith("//"):
                continue
            
            if line == "{":
                level += 1
                continue
            
            if line == "}":
                level -= 1
                continue
            
            match = DATA_REGEX.match(line)
            if match:
                key = match.group(1)
                value = match.group(2)
                
                if key == "name":
                    current_name = value
                elif key == "commonattribs" and value == "4":
                    data.append(current_name)
                    
    
    return data

#
# main program
#

if path.exists(ESC_GIT_DIR):
    subprocess.run(["git", "-C", ESC_GIT_DIR, "pull", "--depth", "1"])
else:
    subprocess.run(["git", "clone", "--depth", "1", ESC_GIT_REPO, ESC_GIT_DIR])

shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
shutil.rmtree(UNIT_PICS_DIR, ignore_errors=True)

os.makedirs(UNIT_PICS_DIR)

for file in ESC_FILES:
    path.join(ESC_GIT_DIR, file)
    run_hpi_extract(EXTRACT_DIR, )
    
    if path.exists(EXTRACT_UNIT_PICS_DIR):
        for pic in os.listdir(EXTRACT_UNIT_PICS_DIR):
            webp_version = change_extension(pic, "webp")
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", EXTRACT_UNIT_PICS_DIR+pic, "-lossless", "1", "-compression_level", "6", UNIT_PICS_DIR+webp_version])
    
    if path.exists(EXTRACT_WEAPONS_DIR):
        for weapon in os.listdir(EXTRACT_WEAPONS_DIR):                    
            weapon_path = path.join(EXTRACT_WEAPONS_DIR, weapon)
            WEAPON_DATA.update(tdf_data(weapon_path))
        
    if path.exists(EXTRACT_UNITS_DIR):
        for unit in os.listdir(EXTRACT_UNITS_DIR):
            if any(unit.startswith(name) for name in EXCLUDE_UNITS):
                continue
                    
            unit_path = path.join(EXTRACT_UNITS_DIR, unit)
            data = fbi_data(unit_path)
            UNIT_DATA[data["unitname"]] = data
            
    if path.exists(EXTRACT_GUIS_DIR):
        for gui in os.listdir(EXTRACT_GUIS_DIR):
            if not gui.lower().endswith("gui"):
                continue
            
            gui_name = gui.split(".")[0]
            gui_page = gui_name[-1]
            gui_name = gui_name[:-1]
            
            gui_path = path.join(EXTRACT_GUIS_DIR, gui)
            try:
                data = gui_data(gui_path)
                if gui_name in GUI_DATA:
                    GUI_DATA[gui_name][int(gui_page)] = data
                elif len(data) > 0:
                    GUI_DATA[gui_name] = {int(gui_page): data}
            except:
                continue
            
    
    shutil.rmtree(EXTRACT_DIR, ignore_errors=True)


for gui in GUI_DATA:
    data = []
    for page in GUI_DATA[gui]:
        data.extend(GUI_DATA[gui][page])
    GUI_DATA[gui] = data

BUILT_BY_DATA = {}

for gui in GUI_DATA:
    for unit in GUI_DATA[gui]:
        if unit in BUILT_BY_DATA:
            BUILT_BY_DATA[unit].append(gui)
        else:
            BUILT_BY_DATA[unit] = [gui]
            
for unit_name in UNIT_DATA:
    unit = UNIT_DATA[unit_name]
    unit["builtby"] = BUILT_BY_DATA.get(unit_name, [])
    unit["builds"] = GUI_DATA.get(unit_name, [])
    
    for category in unit["category"]:
        if category.startswith("LEV"):
            unit["tier"] = int(category[-1])
            break


constructor_map = {
    "kbot": "KBOT",
    "vehicle": "VEHICLE",
    "ship": "SHIP",
    "sub": "SHIP",
    "hovercraft": "HOVERCRAFT",
    "aircraft": "AIRCRAFT",
    "seaplane": "AIRCRAFT"
}

def is_troop(unit):
    for builder in unit["builtby"]:
        if builder["tedclass"] == "PLANT":
            return True
    return False

def is_constructor(unit):
    return unit["tedclass"] == "CNSTR" and "construction" in unit["name"].lower()

def get_constructor_type(unit):
    constructor_type = unit["name"].split()[-1]
    return constructor_map[constructor_type.lower()]

def find_troop_type(unit):
    for plant_name in unit["builtby"]:
        plant = UNIT_DATA[plant_name]
        if plant["tedclass"] == "PLANT":
            for constructor_name in plant["builds"]:
                constructor = UNIT_DATA[constructor_name]
                if is_constructor(constructor):
                    return get_constructor_type(constructor)
    return None
    

for unit_name in UNIT_DATA:
    unit = UNIT_DATA[unit_name]
    ted_class = unit["tedclass"]
    rovi_class = "OTHER"
    
    if ted_class == "COMMANDER":
        rovi_class = "COMMANDER"
        
    elif unit["footprintx"] == 0 and unit["footprintz"] == 0:
        rovi_class = "UPGRADE"
        
    elif ted_class == "PLANT":
        rovi_class = "LAB"
    
    elif ted_class == "METAL":
        rovi_class = "RESOURCE"
    elif ted_class == "ENERGY":
        rovi_class = "RESOURCE"
        
    elif "BLDG" in unit["category"]:
        rovi_class = "BUILDING"
    elif ted_class == "FORT":
        rovi_class = "BUILDING"
    elif ted_class == "SPECIAL":
        rovi_class = "BUILDING"
        
    elif "KBOT" == ted_class:
        rovi_class = "KBOT"
    elif "VTOL" == ted_class:
        rovi_class = "AIRCRAFT"
    elif "SHIP" == ted_class:
        rovi_class = "SHIP"
        
    elif "CTRL_V" in unit["category"]:
        rovi_class = "VEHICLE"
    elif "CTRL_N" in unit["category"]:
        rovi_class = "SHIP"
    elif "CTRL_H" in unit["category"]:
        rovi_class = "HOVERCRAFT"
    elif "CTRL_U" in unit["category"]:
        rovi_class = "SHIP"
    elif "CTRL_K" in unit["category"]:
        rovi_class = "KBOT"
    elif "CTRL_P" in unit["category"]:
        rovi_class = "AIRCRAFT"
        
    elif is_constructor(unit):
        rovi_class = get_constructor_type(unit)
    
    else:
        rovi_class = find_troop_type(unit)
        
                
    unit["roviclass"] = rovi_class
        
        


with open(UNIT_DATA_PATH, "w") as f:
    json.dump(UNIT_DATA, f, indent=4)

with open(WEAPON_DATA_PATH, "w") as f:
    json.dump(WEAPON_DATA, f, indent=4)

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
        
# shutil.rmtree(ESC_GIT_DIR, onerror=on_rm_error)