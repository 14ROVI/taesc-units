import subprocess
import os
from os import path
import shutil
import stat
import re
import json
import platform
import time
from chardet import detect
import requests
import ta_file_decoder
import env

ESC_FILE_EXTENSIONS = (".gp3", ".ufo")
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
EXTRACT_DESTINATION = "./dist/data/"
UNIT_PICS_DIR = EXTRACT_DESTINATION+"unit_icons/"
UNIT_DATA_PATH = EXTRACT_DESTINATION+"units.json"
WEAPON_DATA_PATH = EXTRACT_DESTINATION+"weapons.json"
GUIS_DATA_PATH = EXTRACT_DESTINATION+"guis.json"
META_DATA_PATH = EXTRACT_DESTINATION+"meta.json"

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
    "GOKT3SUPRPOD", "ZZZ",
}
EXCLUDE_WEAPONS = {}
UNIT_DATA = {}
WEAPON_DATA = {}
GUI_DATA = {}
META_DATA = {}


def run_hpi_extract(output_folder, input_file):
    if platform.system().lower() == "windows":
        subprocess.run(["./hpiextract.exe", output_folder, input_file], stdout=subprocess.DEVNULL)
    else:
        subprocess.run(["./hpiextract", output_folder, input_file], stdout=subprocess.DEVNULL)


def change_extension(file_path, new_extension):
    return ".".join(file_path.split(".")[:-1]) + "." + new_extension


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
        encoding = detect(rawdata)["encoding"] or "utf-8"
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


def get_version():
    highest_major = 0
    highest_minor = 0
    highest_patch = 0
    
    for file in os.listdir(ESC_GIT_DIR):
        if file.lower().startswith("gold"):
            numbers = file[5:-4].split("_")
            major = int(numbers[0])
            minor = int(numbers[1])
            patch = int(numbers[2])
            
            if major > highest_major:
                highest_major = major
                highest_minor = minor
                highest_patch = patch
            elif major == highest_major and minor > highest_minor:
                highest_minor = minor
                highest_patch = patch
            elif major == highest_major and minor == highest_minor and patch > highest_patch:
                highest_patch = patch
    
    return (highest_major, highest_minor, highest_patch)

#
# main program
#

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
    
    
def main():

    shutil.rmtree(ESC_GIT_DIR, onexc=on_rm_error)
    subprocess.run(["git", "clone", "--depth", "1", ESC_GIT_REPO, ESC_GIT_DIR])

    shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
    shutil.rmtree(UNIT_PICS_DIR, ignore_errors=True)

    if not path.exists(EXTRACT_DESTINATION):
        os.makedirs(EXTRACT_DESTINATION)
    os.makedirs(UNIT_PICS_DIR)

    print(get_version())

    for file in os.listdir(ESC_GIT_DIR):
        if not file.endswith(ESC_FILE_EXTENSIONS):
            continue
        
        run_hpi_extract(EXTRACT_DIR, path.join(ESC_GIT_DIR, file))
        
        if path.exists(EXTRACT_UNIT_PICS_DIR):
            processes = []
            for pic in os.listdir(EXTRACT_UNIT_PICS_DIR):
                webp_version = change_extension(pic, "webp")
                p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", EXTRACT_UNIT_PICS_DIR+pic, "-lossless", "1", "-compression_level", "6", UNIT_PICS_DIR+webp_version])
                processes.append(p)
            for p in processes:
                p.wait()
        
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
                
                if not gui_page.isnumeric():
                    continue
                
                gui_path = path.join(EXTRACT_GUIS_DIR, gui)
                data = gui_data(gui_path)
                if gui_name in GUI_DATA:
                    GUI_DATA[gui_name][int(gui_page)] = data
                elif len(data) > 0:
                    GUI_DATA[gui_name] = {int(gui_page): data}
                
        
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
        unit["category"] = unit["category"].strip().split()
        if "yardmap" in unit:
            unit["yardmap"] = unit["yardmap"].strip().split()
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


    with open(UNIT_DATA_PATH, "w") as f:
        json.dump(UNIT_DATA, f, indent=4)

    with open(WEAPON_DATA_PATH, "w") as f:
        json.dump(WEAPON_DATA, f, indent=4)
        
    with open(META_DATA_PATH, "w") as f:
        META_DATA = {
            "updated_at": int(time.time()),
            "success": True
        }
        json.dump(META_DATA, f, indent=4)
            
    # shutil.rmtree(ESC_GIT_DIR, onerror=on_rm_error)
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        requests.post(
            env.WEBHOOK_URL,
            data = {"content": f"<@{env.USER_ID}> something wrong happened extracting ta files :(:\n```\n{e}```"}
        )
        raise e