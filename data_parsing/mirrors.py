import env
import json
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timezone

with open(env.META_FILE, "r") as f:
    metadata = json.load(f)

with requests.get("https://taesc.tauniverse.com/?p=downloads") as r:
    soup = BeautifulSoup(r.text, "html.parser")
    
latest_download_url = soup.find("a", text="DOWNLOAD")["href"]
date_published = soup.find("a", text="DOWNLOAD").parent.text.split("Date: ")[1].split("Size:")[0].replace("st,", "").replace("nd,", "").replace("rd,", "").replace("th,", "")
date_published = datetime.strptime(date_published, "%B %d %Y")
date_published = date_published.replace(tzinfo=timezone.utc).timestamp()
date_published = int(date_published)

file_name = latest_download_url.split("/")[-1]

if metadata.get("latest_published_at", 0) != date_published:
    with requests.get(f"https://taesc.tauniverse.com/{latest_download_url}") as r:
        with open(env.MIRRORS_DIR / file_name, "wb") as ldf:
            ldf.write(r.content)
            
    for match in re.finditer(r"(\d).(\d).(\d)", file_name):
        latest_version = [int(n) for n in match.groups()]
        
    metadata["latest_published_at"] = date_published
    metadata["latest_version"] = latest_version

    for file in env.MIRRORS_DIR.iterdir():
        for match in re.finditer(r"(\d).(\d).(\d)", file.name):
            version = [int(n) for n in match.groups()]
        
        added = False
        
        for group in  metadata["versions"]:
            if group["version"] == version:
                group["mirrors"][file.name] = file.stat().st_size
                added = True

        if not added:
                metadata["versions"].append({
                "version": version,
                "mirrors": {file.name: file.stat().st_size}
            })
            

    with open(env.META_FILE, "w") as f:
        json.dump(metadata, f, indent=4)
