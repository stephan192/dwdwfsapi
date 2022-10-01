# dwdwfsapi
Python client to retrieve data provided by DWD via their geoserver WFS API

The DWD (Deutscher Wetterdienst) publishes various weather information for Germany.
The data is published via their [Geoserver](https://maps.dwd.de). For a more information have a look [here](https://www.dwd.de/DE/leistungen/geodienste/geodienste.html) and [here](https://maps.dwd.de/geoserver/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities).

## Install
```
pip install dwdwfsapi
```

## Usage
The WFS API currently consists only of one module for retrieving the current weather warnings.

### Weather warnings module

#### Quickstart example
Python code
```
from dwdwfsapi import DwdWeatherWarningsAPI
dwd = DwdWeatherWarningsAPI('813073088')

if dwd.data_valid:
    print(f"Warncell id: {dwd.warncell_id}")
    print(f"Warncell name: {dwd.warncell_name}")
    print(f"Number of current warnings: {len(dwd.current_warnings)}")
    print(f"Current warning level: {dwd.current_warning_level}")
    print(f"Number of expected warnings: {len(dwd.expected_warnings)}")
    print(f"Expected warning level: {dwd.expected_warning_level}")
    print(f"Last update: {dwd.last_update}")
    print('-----------')
    for warning in dwd.current_warnings:
        print(warning)
        print('-----------')
    for warning in dwd.expected_warnings:
        print(warning)
        print('-----------')
```

Result (formatted for better readability)
```
Warncell id: 813073088
Warncell name: Stadt Stralsund
Number of current warnings: 0
Current warning level: 0
Number of expected warnings: 1
Expected warning level: 1
Last update: 2020-04-18 17:57:29.274000+00:00
-----------
{
    'start_time': datetime.datetime(2020, 4, 18, 23, 0, tzinfo=datetime.timezone.utc),
    'end_time': datetime.datetime(2020, 4, 19, 5, 0, tzinfo=datetime.timezone.utc),
    'event': 'FROST',
    'event_code': 22,
    'headline': 'Amtliche WARNUNG vor FROST',
    'description': 'Es tritt leichter Frost um 0 °C auf. In Bodennähe wird leichter Frost bis -4 °C erwartet.',
    'instruction': None, 'level': 1,
    'parameters':
    {
        'Lufttemperatur': '~0 [°C]',
        'Bodentemperatur': '>-4 [°C]'
    },
    'color': '#ffff00'
}
-----------
```

#### Detailed description
**Methods:**
- **`__init__(identifier)`**  
  Create a new weather warnings API class instance  
  
  The `identifier` can either be a so called `warncell id` (int), a `warncell name` (str) or a `gps location` (tuple). 
  It is heavily advised to use `warncell id` over `warncell name` because the name is not unique in some cases. The 
  `gps location` consists of the latitude and longitude in this order. Keeping this order for the tuple is important for
  the query to work correctly.  

  A list auf valid warncell ids and names can be found [here](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_warncellids_csv.html). 
  Some of the warncells are outdated but still listed. If init fails search the list for a similar sounding warncell.  

  Method `update()` is automatically called at the end of a successfull init.  

- **`update()`**  
  Update data by querying DWD server and parsing result  
  
  Function should be called regularly, e.g. every 15minutes, to update the data stored in the class attributes.

**Attributes (read only):**
- **`data_valid : bool`**  
  A flag wether or not the other attributes contain valid values

- **`warncell_id : int`**  
  The id of the selected warncell

- **`warncell_name : str`**  
  The name of the selected warncell  
  
  If the name is not unique `" (not unique used ID)!"` will be added to the name

- **`last_update : datetime`**  
  The UTC timestamp of the last update

- **`current_warning_level : int`**  
  Highest currently active warning level  
  
  Range: 0 (=no warning) to 4 (=extreme weather)

- **`current_warnings : list of dicts`**  
  Dictionary containing all currently active warnings ("Wetterwarnungen", urgency="immediate")
  
  See section warning dictionary for more details

- **`expected_warning_level : int`**  
  Highest expected warning level  
  
  Range: 0 (=no warning) to 4 (=extreme weather)

- **`expected_warnings : list of dicts`**  
  Dictionary containing all expected warnings ("Vorabinformationen", urgency="future")
  
  See section warning dictionary for more details
    expected_warnings : dict

**Warning dictionary**
- **`start_time : datetime`**  
  UTC timestamp when the warning starts

- **`end_time : datetime`**  
  UTC timestamp when the warning ends

- **`event: str`**  
  String representation of the warning event

- **`event_code: int`**  
  Integer representation of the warning event
  
  For more details have a look [here](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/gesamtueberblickII.pdf?__blob=publicationFile&v=3)

- **`headline : str`**  
  The official warning headline

- **`description : str`**  
  A details warning description

- **`instruction : str`**  
  Instructions and safety notices

- **`urgency : str`**  
  Warning urgency (either "immediate" or "future")

- **`level : int`**  
  Warning level  
  
  Range: 0 (=no warning) to 4 (=extreme weather)

- **`parameters : dict`**  
  Dictionary containing warning specific parameters  
  
  For more details have a look [here](https://www.dwd.de/DE/leistungen/opendata/help/warnungen/cap_dwd_profile_de_pdf_1_11.pdf?__blob=publicationFile&v=3)

- **`color : str`**  
  Warning color formatted #rrggbb
