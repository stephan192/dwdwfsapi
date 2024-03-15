# dwdwfsapi
Python client to retrieve data provided by DWD via their geoserver WFS API

The DWD (Deutscher Wetterdienst) publishes various weather information for Germany.
The data is published via their [Geoserver](https://maps.dwd.de). For a more information have a look [here](https://www.dwd.de/DE/leistungen/geodienste/geodienste.html) and [here](https://maps.dwd.de/geoserver/wfs?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities).

## Install
```
pip install dwdwfsapi
```

## Usage
The WFS API currently consists of three modules. One for retrieving the current weather warnings, one for retrieving the bio weather forecast and one for retrieving the pollen flight forecast.

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

  A list of valid warncell ids and names can be found in [warncells.md](https://github.com/stephan192/dwdwfsapi/blob/master/docs/warncells.md).  

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
  
  If the name is not unique `" (not unique use ID!)"` will be added to the name

- **`last_update : datetime`**  
  Timestamp of the last update

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

**Warning dictionary**
- **`start_time : datetime`**  
  Timestamp when the warning starts

- **`end_time : datetime`**  
  Timestamp when the warning ends

- **`event: str`**  
  String representation of the warning event

- **`event_code: int`**  
  Integer representation of the warning event

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

- **`color : str`**  
  Warning color formatted #rrggbb

### Bio weather module

#### Quickstart example
Python code
```
from dwdwfsapi import DwdBioWeatherAPI
bio = DwdBioWeatherAPI(8)

if bio.data_valid:
    for k, v in bio.forecast_data.items():
        print(f"{k} - {v['name']}")
        for entry in v["forecast"]:
            print(f"\t{entry['start_time']} : {entry['color']} - {entry['level']} = {entry['impact']}")
```

Result
```
1 - allgemeine Befindensbeeinträchtigungen
        2024-03-15 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-15 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-16 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-16 12:00:00+00:00 : #006eff - 0 = positiver Einfluss
        2024-03-17 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 12:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
2 - Asthma
        2024-03-15 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-15 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-16 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-16 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-17 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
3 - Herz- und Kreislaufgeschehen (hypotone Form)
        2024-03-15 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-15 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-16 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-16 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-17 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 12:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
4 - Herz- und Kreislaufgeschehen (hypertone Form)
        2024-03-15 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-15 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-16 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-16 12:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
5 - rheumatische Beschwerden (degenerativ)
        2024-03-15 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-15 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-16 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-16 12:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
6 - rheumatische Beschwerden (entzündlich)
        2024-03-15 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-15 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-16 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-16 12:00:00+00:00 : #37ba29 - 1 = kein Einfluss
        2024-03-17 00:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
        2024-03-17 12:00:00+00:00 : #ffff00 - 2 = geringe Gefährdung
```

#### Detailed description
**Methods:**
- **`__init__(identifier)`**  
  Create a new bio weather API class instance  
  
  The `identifier` can either be a so called `cell id` (int) or a `cell name` (str). 
  It is heavily advised to use `cell id` over `cell name` because the name is not unique in some cases.

  A list of valid warncell ids and names can be found in [warncells.md](https://github.com/stephan192/dwdwfsapi/blob/master/docs/biocells.md).  

  Method `update()` is automatically called at the end of a successfull init.  

- **`update()`**  
  Update data by querying DWD server and parsing result  
  
  Function should be called regularly, e.g. every 15minutes, to update the data stored in the class attributes.

**Attributes (read only):**
- **`data_valid : bool`**  
  A flag wether or not the other attributes contain valid values

- **`cell_id : int`**  
  The id of the selected cell

- **`cell_name : str`**  
  The name of the selected ncell  
  
  If the name is not unique `" (not unique use ID!)"` will be added to the name

- **`last_update : datetime`**  
  Timestamp of the last update

- **`forecast_data : dict`**  
  Dictionary containing all forecast data
  
  See section forecast data dictionary for more details

**Forecast data dictionary**
- **`key : int`**  
  Data type

- **`name : str`**  
  String representation of the data type

- **`forecast : list of dicts`**  
  List containing the forecast data
  
  See section forecast dictionary for more details

**Forecast dictionary**
- **`start_time : datetime`**  
  Timestamp when the forecast starts

- **`level : int`**  
  Impact level (0 - 3)

- **`impact : str`**  
  String representation of the impact level

- **`color : str`**  
  Forecast color formatted #rrggbb

### Pollen flight module

#### Quickstart example
Python code
```
from dwdwfsapi import DwdPollenFlightAPI
dwd = DwdPollenFlightAPI(41)

if dwd.data_valid:
    for k, v in dwd.forecast_data.items():
        print(f"{k} - {v['name']}")
        for entry in v["forecast"]:
            print(f"\t{entry['start_time']} : {entry['color']} - {entry['level']} = {entry['impact']}")
```

Result
```
1 - Hasel
        2024-03-15 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-16 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-17 00:00:00+00:00 : #ffffff - 0 = keine
2 - Erle
        2024-03-15 00:00:00+00:00 : #fee391 - 2 = gering
        2024-03-16 00:00:00+00:00 : #fee391 - 3 = gering bis mittel
        2024-03-17 00:00:00+00:00 : #fee391 - 3 = gering bis mittel
8 - Esche
        2024-03-15 00:00:00+00:00 : #fee391 - 2 = gering
        2024-03-16 00:00:00+00:00 : #fee391 - 2 = gering
        2024-03-17 00:00:00+00:00 : #fee391 - 3 = gering bis mittel
3 - Birke
        2024-03-15 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-16 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-17 00:00:00+00:00 : #ffffff - 2 = gering
4 - Gräser
        2024-03-15 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-16 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-17 00:00:00+00:00 : #ffffff - 0 = keine
5 - Roggen
        2024-03-15 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-16 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-17 00:00:00+00:00 : #ffffff - 0 = keine
6 - Beifuß
        2024-03-15 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-16 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-17 00:00:00+00:00 : #ffffff - 0 = keine
7 - Ambrosia
        2024-03-15 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-16 00:00:00+00:00 : #ffffff - 0 = keine
        2024-03-17 00:00:00+00:00 : #ffffff - 0 = keine
```

#### Detailed description
**Methods:**
- **`__init__(identifier)`**  
  Create a new pollen flight API class instance  
  
  The `identifier` can either be a so called `cell id` (int) or a `cell name` (str). 
  It is heavily advised to use `cell id` over `cell name` because the name is not unique in some cases.

  A list of valid warncell ids and names can be found in [warncells.md](https://github.com/stephan192/dwdwfsapi/blob/master/docs/pollencells.md).  

  Method `update()` is automatically called at the end of a successfull init.  

- **`update()`**  
  Update data by querying DWD server and parsing result  
  
  Function should be called regularly, e.g. every 15minutes, to update the data stored in the class attributes.

**Attributes (read only):**
- **`data_valid : bool`**  
  A flag wether or not the other attributes contain valid values

- **`cell_id : int`**  
  The id of the selected cell

- **`cell_name : str`**  
  The name of the selected ncell  
  
  If the name is not unique `" (not unique use ID!)"` will be added to the name

- **`last_update : datetime`**  
  Timestamp of the last update

- **`forecast_data : dict`**  
  Dictionary containing all forecast data
  
  See section forecast data dictionary for more details

**Forecast data dictionary**
- **`key : int`**  
  Data type

- **`name : str`**  
  String representation of the data type

- **`forecast : list of dicts`**  
  List containing the forecast data
  
  See section forecast dictionary for more details

**Forecast dictionary**
- **`start_time : datetime`**  
  Timestamp when the forecast starts

- **`level : int`**  
  Impact level (0 - 6)

- **`impact : str`**  
  String representation of the impact level

- **`color : str`**  
  Forecast color formatted #rrggbb
