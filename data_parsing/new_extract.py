import env
import ta_file_decoder
import cob_interpreter

import subprocess
import os
import json
import time
import platform
from PIL import Image
from chardet import detect
from git import Repo


constructor_map = {
    "kbot": "KBOT",
    "vehicle": "VEHICLE",
    "ship": "SHIP",
    "sub": "SHIP",
    "hovercraft": "HOVERCRAFT",
    "aircraft": "AIRCRAFT",
    "seaplane": "AIRCRAFT"
}
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
    "GOKT3SUPRPOD", "ZZZ"
}
EXCLUDE_WEAPONS = {}
BUILT_BY_DATA = {}
UNIT_DATA = {}
WEAPON_DATA = {}
GUI_DATA = {}

def change_extension(file_path, new_extension):
    return ".".join(file_path.split(".")[:-1]) + "." + new_extension

def run_hpi_extract(output_folder, input_file):
    print(f"Extracting {input_file}")
    
    if platform.system().lower() == "windows":
        subprocess.run(["./data_parsing/hpiextract.exe", output_folder, input_file], stdout=subprocess.DEVNULL)
    else:
        subprocess.run(["./hpiextract", output_folder, input_file], stdout=subprocess.DEVNULL)

def fbi_data(file_path):
    data = {}
    
    with open(file_path, "rb") as f:
        rawdata = f.read()
        encoding = detect(rawdata)["encoding"]
        if encoding is None: return data
        text = rawdata.decode(encoding=encoding)
        data = ta_file_decoder.decode(text)

        data = {
            k.lower(): v for k, v in data["UNITINFO"].items()
        }
    
    return data

def tdf_data(file_path):
    data = {}
    
    with open(file_path, "rb") as f:
        rawdata = f.read()
        encoding = detect(rawdata)["encoding"]
        if encoding is None: return data
        text = rawdata.decode(encoding=encoding)
        data = ta_file_decoder.decode(text)

        for weapon_name in data:
            data[weapon_name] = {
                k.lower(): v for k, v in data[weapon_name].items()
            }
    
    return data

def gui_data(file_path):
    data = []
    
    with open(file_path, "rb") as f:
        rawdata = f.read()
        encoding = detect(rawdata)["encoding"]
        if encoding is None: return data
        text = rawdata.decode(encoding=encoding)
        gui_data = ta_file_decoder.decode(text)
        
        for gadget in gui_data.values():
            name = gadget["COMMON"]["name"]
            width = gadget["COMMON"]["width"]
            height = gadget["COMMON"]["height"]
            commonattribs = gadget["COMMON"]["commonattribs"]
            attribs = gadget["COMMON"]["attribs"]
            greyed_out = gadget.get("grayedout", 0)
            
            if greyed_out:
                continue
            
            add = False
            
            if width == height and (width == 64 or width == 128):
                add = True
            elif commonattribs == 4:
                add = True
            elif attribs == 32:
                add = True
                
            if add:
                data.append(name)
    
    return data

#
# program
#


try:
    repo = Repo(env.ESC_GIT_DIR)
except:
    os.makedirs(env.ESC_GIT_DIR, exist_ok=True)
    repo = Repo.clone_from("https://git.taforever.com/ta-forever/taesc.git", env.ESC_GIT_DIR)

# update git with info of origin
current = repo.head.commit
origin = repo.remote("origin")
origin.pull()
updated = current != repo.head.commit

# if not updated:
#     print("esc not updated, no need to update website!")
#     exit()

# remove the old content and extract new content

# shutil.rmtree(env.EXTRACT_DIR, ignore_errors=True)
# os.makedirs(env.EXTRACT_DIR, exist_ok=True)
# for file in os.listdir(env.ESC_GIT_DIR):
#     if file.lower().endswith((".gp3", ".ufo")):
#         run_hpi_extract(env.EXTRACT_DIR, env.ESC_GIT_DIR / file)

# convert all unit pics into webp
print("Converting unit pics")
# for file in os.listdir(env.EXTRACT_DIR / "unitpicE"):
#     if file.lower().endswith((".pcx")):
#         with Image.open(env.EXTRACT_DIR / "unitpicE" / file) as img:
#             img.save(env.UNIT_ICONS_DIR / change_extension(file, "webp"))
               
# extract unit data
print("loading unit data")
for unit in os.listdir(env.EXTRACT_DIR / "unitsE"):
    if any(unit.startswith(name) for name in EXCLUDE_UNITS):
        continue
    
    data = fbi_data(env.EXTRACT_DIR / "unitsE" / unit)
    UNIT_DATA[data["unitname"]] = data
    
# extract weapon data
print("loading weapon data")
for weapon in os.listdir(env.EXTRACT_DIR / "weaponE"):
    WEAPON_DATA.update(tdf_data(env.EXTRACT_DIR / "weaponE" / weapon))
    
# extract gui data
print("loading gui data")
for gui in os.listdir(env.EXTRACT_DIR / "guiE"):
    if not gui.lower().endswith("gui"):
        continue
    
    gui_name = gui.split(".")[0]
    gui_page = gui_name[-1]
    gui_name = gui_name[:-1]
    
    if not gui_page.isnumeric():
        continue
    
    data = gui_data(env.EXTRACT_DIR / "guiE" / gui)
    if gui_name in GUI_DATA:
        GUI_DATA[gui_name].extend(data)
    elif len(data) > 0:
        GUI_DATA[gui_name] = data


# calculate true reload speeds
for unit_name in UNIT_DATA:
    unit = UNIT_DATA[unit_name]
    if not ("weapon1" in unit or "weapon2" in unit or "weapon3" in unit):
        continue
    
    print(unit_name)
    import logging
    # logging.basicConfig(level=logging.INFO)
    with open(env.EXTRACT_DIR / "scripts" / f"{unit_name}.cob", mode="rb") as f:
        data = f.read()
        if "weapon1" in unit:
            weapon = WEAPON_DATA[unit["weapon1"]] 
            min_reload = int(weapon["reloadtime"] * 1000)
            in_water = weapon.get("waterweapon", False)
            unit["weapon1reload"] = cob_interpreter.calculate_reload_speed(data, "primary", min_reload, in_water)
            print(min_reload, unit["weapon1reload"])
        if "weapon2" in unit:
            weapon = WEAPON_DATA[unit["weapon2"]]
            min_reload = int(weapon["reloadtime"] * 1000)
            in_water = weapon.get("waterweapon", False)
            unit["weapon2reload"] = cob_interpreter.calculate_reload_speed(data, "secondary", min_reload, in_water)
            print(min_reload, unit["weapon2reload"])
        if "weapon3" in unit:
            weapon = WEAPON_DATA[unit["weapon3"]]
            min_reload = int(weapon["reloadtime"] * 1000)
            in_water = weapon.get("waterweapon", False)
            unit["weapon3reload"] = cob_interpreter.calculate_reload_speed(data, "tertiary", min_reload, in_water)
            print(min_reload, unit["weapon3reload"])

print("misc calculations")

for gui in GUI_DATA:
    for unit in GUI_DATA[gui]:
        if unit in BUILT_BY_DATA:
            BUILT_BY_DATA[unit].append(gui)
        else:
            BUILT_BY_DATA[unit] = [gui]
            
for unit_name in UNIT_DATA:
    unit = UNIT_DATA[unit_name]
    unit["category"] = unit["category"].strip().split()
    if "yardmap" in unit:
        unit["yardmap"] = unit["yardmap"].strip().split()
    unit["builtby"] = BUILT_BY_DATA.get(unit_name, [])
    unit["builds"] = GUI_DATA.get(unit_name, [])
    
    for category in unit["category"]:
        if category.startswith("LEV"):
            unit["tier"] = int(category[-1])
            break

def is_troop(unit):
    for builder in unit["builtby"]:
        if builder["tedclass"] == "PLANT":
            return True
    return False

def is_constructor(unit):
    return (
        unit["tedclass"] == "CNSTR"
        and (
            "construction" in unit["name"].lower()
            or "mobile factory" in unit["name"].lower()
            or "builder" in unit["name"].lower()
        ))

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
    return "OTHER"
    

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


with open(env.UNITS_FILE, "w") as f:
    json.dump(UNIT_DATA, f, indent=4)

with open(env.WEAPONS_FILE, "w") as f:
    json.dump(WEAPON_DATA, f, indent=4)

with open(env.GUIS_FILE, "w") as f:
    json.dump(GUI_DATA, f, indent=4)
    
with open(env.META_FILE, "r") as f:
    META_DATA = json.load(f)
    META_DATA["updated_at"] = int(time.time())

with open(env.META_FILE, "w") as f:
    json.dump(META_DATA, f, indent=4)