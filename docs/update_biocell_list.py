"""DWD WFS API - Utility module to update biocells.md."""

from __future__ import annotations

import json

import requests


def fetch_json() -> dict:
    """Fetch data via json."""
    url = (
        "https://maps.dwd.de/geoserver/dwd/ows?service=WFS"
        + "&version=2.0.0&request=GetFeature&typeName="
        + "dwd:Biowettergebiete"
        + "&OutputFormat=application/json"
    )
    response = requests.get(url=url, timeout=10.0)
    return response.json()


def parse_json(data: dict) -> tuple[str, str]:
    """Parse json data."""
    stations = []
    for x in data["features"]:
        cellid = x["properties"]["GF"]
        name = x["properties"]["GEN"]
        stations.append((cellid, name))
    return stations


# Fetch and sort all available stations
all_stations = []
print("Fetching Biowettergebiete")
all_stations.extend(parse_json(fetch_json()))
all_stations.sort(key=lambda x: x[0])

print("Updating biocells.md")
with open("biocells.md", "w", encoding="utf-8") as f:
    print("| Cell ID | Name |", file=f)
    print("|---------|------|", file=f)
    for cell in all_stations:
        output = "| " + str(cell[0]) + " | " + cell[1] + " |"
        print(output, file=f)
    f.close()

all_stations_dict = {}
for cell in all_stations:
    all_stations_dict[cell[0]] = cell[1]

print("Updating biocells.json")
with open("biocells.json", "w", encoding="utf-8") as f:
    json.dump(all_stations_dict, f, indent=4, ensure_ascii=False)
    f.close()
