"""DWD WFS API - Utility module to update warncells.md."""

from __future__ import annotations

import urllib.parse

import requests

AREAS = {
    "Gemeinden": "dwd:Warngebiete_Gemeinden",
    "Landkreise": "dwd:Warngebiete_Kreise",
    "Binnenseen": "dwd:Warngebiete_Binnenseen",
    "Küste": "dwd:Warngebiete_Kueste",
}


def fetch_json(layer: str) -> dict:
    """Fetch data via json."""
    url = (
        "https://maps.dwd.de/geoserver/dwd/ows?service=WFS"
        + "&version=2.0.0&request=GetFeature&typeName="
        + urllib.parse.quote(layer)
        + "&OutputFormat=application/json"
    )
    response = requests.get(url=url, timeout=10.0)
    return response.json()


def parse_json(section: str, data: dict) -> tuple[str, str, str]:
    """Parse json data."""
    stations = []
    for x in data["features"]:
        cellid = str(x["properties"]["WARNCELLID"])
        name = x["properties"]["NAME"]
        stations.append((cellid, section, name))
    return stations


# Fetch and sort all available stations
all_stations = []
for category, area in AREAS.items():
    print(f"Fetching {category}")
    all_stations.extend(parse_json(category, fetch_json(area)))
all_stations.sort(key=lambda x: x[0])

print("Updating warncells.md")
with open("warncells.md", "w", encoding="utf-8") as f:
    print("| Warncell ID | Gebietstyp | Name |", file=f)
    print("|-------------|------------|------|", file=f)
    for warncell in all_stations:
        output = "| " + warncell[0] + " | " + warncell[1] + " | " + warncell[2] + " |"
        print(output, file=f)

    f.close()
