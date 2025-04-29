
import os

to_find = 0x10023004.to_bytes(4, "little") + 0x00000006.to_bytes(4, "little")

def find(fp):
    with open(fp, "rb") as f:
        s = f.read()
    for i in range(0, len(s), 4):
        if s[i:i+len(to_find)] == to_find:
            print(fp, i)

find("ARMAMPH.cob")

# for root, dirs, files in os.walk("extracted_files/totala1"):
#     for file in files:
#         if file.lower().endswith(".cob"):
#             find(root+"/"+file)
        
    
