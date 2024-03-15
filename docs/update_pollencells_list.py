"""DWD WFS API - Utility module to update pollencells.md."""

from __future__ import annotations

import requests


def fetch_json() -> dict:
    """Fetch data via json."""
    url = (
        "https://maps.dwd.de/geoserver/dwd/ows?service=WFS"
        + "&version=2.0.0&request=GetFeature&typeName="
        + "dwd:Pollenfluggebiete"
        + "&OutputFormat=application/json"
    )
    print(url)
    response = requests.get(url=url, timeout=10.0)
    return response.json()


def parse_json(data: dict) -> tuple[str, str]:
    """Parse json data."""
    stations = []
    for x in data["features"]:
        cellid = x["properties"]["GF"]
        name = x["properties"]["GEN"]
        new_entry = (cellid, name)
        if new_entry not in stations:
            stations.append(new_entry)
    return stations


# Fetch and sort all available stations
all_stations = []
print("Fetching Pollenfluggebiete")
all_stations.extend(parse_json(fetch_json()))
all_stations.sort(key=lambda x: x[0])

print("Updating pollencells.md")
with open("pollencells.md", "w", encoding="utf-8") as f:
    print("| Cell ID | Name |", file=f)
    print("|---------|------|", file=f)
    for cell in all_stations:
        output = "| " + str(cell[0]) + " | " + cell[1] + " |"
        print(output, file=f)

    f.close()
