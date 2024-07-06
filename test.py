import json

with open("./data/units.json") as uf:
    units = json.load(uf)
    
    air_units = [unit["unitname"] for unit in units.values() if unit["roviclass"] == "AIRCRAFT"]
    
with open("./data/weapons.json") as wf:
    weapons = json.load(wf)
    
    aa_weapons = [weapon["name"] for weapon in weapons.values() if set(weapon["damage"].keys()).issuperset(air_units)]
    print(aa_weapons)