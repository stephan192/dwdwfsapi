# -*- coding: utf-8 -*-

"""Python client to retrieve weather warnings from DWD."""

# pylint: disable=c-extension-no-member
import datetime
import ciso8601
from .core import query_dwd


def convert_warning_data(data_in):
    """Convert the data received from DWD."""
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    weather_severity_mapping = {
        "minor": 1,
        "moderate": 2,
        "severe": 3,
        "extreme": 4,
    }

    # Make all keys lowercase
    data_in = {k.lower(): v for k, v in data_in.items()}

    # Default init
    data_out = {
        "start_time": None,
        "end_time": None,
        "event": None,
        "event_code": 0,
        "headline": None,
        "description": None,
        "instruction": None,
        "level": 0,
        "parameters": None,
        "color": "#000000",
    }

    # Convert data
    if "onset" in data_in:
        try:
            data_out["start_time"] = ciso8601.parse_datetime(data_in["onset"])
        except:  # pylint: disable=bare-except # noqa: E722
            data_out["start_time"] = None
    if "expires" in data_in:
        try:
            data_out["end_time"] = ciso8601.parse_datetime(data_in["expires"])
        except:  # pylint: disable=bare-except # noqa: E722
            data_out["end_time"] = None
    if "event" in data_in:
        data_out["event"] = data_in["event"]
    if "ec_ii" in data_in:
        try:
            data_out["event_code"] = int(data_in["ec_ii"])
        except:  # pylint: disable=bare-except # noqa: E722
            data_out["event_code"] = 0
    if "headline" in data_in:
        data_out["headline"] = data_in["headline"]
    if "description" in data_in:
        data_out["description"] = data_in["description"]
    if "instruction" in data_in:
        data_out["instruction"] = data_in["instruction"]
    if "severity" in data_in:
        try:
            if data_in["severity"].lower() in weather_severity_mapping:
                data_out["level"] = weather_severity_mapping[
                    data_in["severity"].lower()
                ]
        except:  # pylint: disable=bare-except # noqa: E722
            data_out["level"] = 0
    if "parametername" in data_in and "parametervalue" in data_in:
        # Depending on the query the keys and values are either seperated
        # by , or ;
        try:
            if "," in data_in["parametername"]:
                keys = data_in["parametername"].split(",")
                values = data_in["parametervalue"].split(",")
            else:
                keys = data_in["parametername"].split(";")
                values = data_in["parametervalue"].split(";")
            data_out["parameters"] = dict(zip(keys, values))
        except:  # pylint: disable=bare-except # noqa: E722
            data_out["parameters"] = None
    if "ec_area_color" in data_in:
        try:
            colors = data_in["ec_area_color"].split(" ")
            data_out["color"] = f"#{int(colors[0]):02x}{int(colors[1]):02x}"
            data_out["color"] += f"{int(colors[2]):02x}"
        except:  # pylint: disable=bare-except # noqa: E722
            data_out["color"] = "#000000"

    return data_out


class DwdWeatherWarningsAPI:
    """
    Class for retrieving weather warnings from DWD.

    Attributes:
    -----------
    data_valid : bool
        a flag wether or not the other attributes contain valid values
    warncell_id : int
        the id of the selected warncell
    warncell_name : str
        the name of the selected warncell
    last_update : datetime
        the UTC timestamp of the last update
    current_warning_level : int
        highest currently active warning level (0 - 4)
    current_warnings : list of dicts
        list of dictionaries containing all currently active warnings
        NOTE: not every warning has all keys
        start_time : datetime
            UTC timestamp when the warning starts
        end_time : datetime
            UTC timestamp when the warning ends
        event: str
            string representation of the warning event
        event_code: int
            integer representation of the warning event
        headline : str
            the official warning headline
        description : str
            a details warning description
        instruction : str
            instructions and safety notices
        level : int
            warning level (0 - 4)
        parameters : dict
            dictionary containing warning specific parameters
            NOTE: too specific to be listed here
        color : str
            warning color formatted #rrggbb
    expected_warning_level : int
        highest expected warning level (0 - 4)
    expected_warnings : list of dicts
        list of dictionaries containung all expected warnings
        dictionary content is identical to current_warnings
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, identifier):
        """
        Init DWD weather warnings.

        Parameters
        ----------
        identifier : str or int
            a valid warncell id or name
            https://www.dwd.de/DE/leistungen/opendata/help/warnungen/
                    cap_warncellids_csv.html
            NOTE: Some of the warncells are outdated but still listed.
                  If init fails search the list for a similar sounding
                  warncell.
        """
        self.data_valid = False
        self.warncell_id = None
        self.warncell_name = None
        self.__query = None
        self.last_update = None
        self.current_warning_level = None
        self.current_warnings = None
        self.expected_warning_level = None
        self.expected_warnings = None

        # Identifier must be either integer or string
        if not isinstance(identifier, (int, str)):
            return

        self.__generate_query(identifier)
        self.update()

    def __bool__(self):
        """Return the data_valid attribute."""
        return self.data_valid

    def __len__(self):
        """Return the sum of current and expected warnings."""
        if self.data_valid:
            length = len(self.current_warnings) + len(self.expected_warnings)
        else:
            length = 0
        return length

    def __str__(self):
        """Return a short overview about the actual status."""
        if self.data_valid:
            retval = f"{len(self.current_warnings)} current and"
            retval += f" {len(self.expected_warnings)} expected warnings"
            retval += f" issued by DWD for '{self.warncell_name}'"
        else:
            retval = "No valid data available"
        return retval

    def update(self):
        """Update data by querying DWD server and parsing result."""
        if self.__query is None:
            return

        json_data = query_dwd(**self.__query)

        if json_data is not None:
            self.__parse_result(json_data)
        else:
            self.data_valid = False
            self.last_update = None
            self.current_warning_level = None
            self.current_warnings = None
            self.expected_warning_level = None
            self.expected_warnings = None

    def __generate_query(self, identifier):
        """Determine the warning region to which the identifier belongs."""
        weather_warnings_query_mapping = {
            "dwd:Warngebiete_Gemeinden": "dwd:Warnungen_Gemeinden",
            "dwd:Warngebiete_Kreise": "dwd:Warnungen_Landkreise",
            "dwd:Warngebiete_See": "dwd:Warnungen_See",
            "dwd:Warngebiete_Binnenseen": "dwd:Warnungen_Binnenseen",
            "dwd:Warngebiete_Kueste": "dwd:Warnungen_Kueste",
        }

        region_query = {}
        # Numbers represent warncell ids
        if isinstance(identifier, int) or identifier.isnumeric():
            region_query["CQL_FILTER"] = f"WARNCELLID='{identifier}'"
        else:
            region_query["CQL_FILTER"] = f"NAME='{identifier}'"

        for region in weather_warnings_query_mapping:
            region_query["typeName"] = region
            result = query_dwd(**region_query)
            if result is not None:
                if result["numberReturned"] > 0:
                    self.warncell_id = result["features"][0]["properties"][
                        "WARNCELLID"
                    ]
                    self.warncell_name = result["features"][0]["properties"][
                        "NAME"
                    ]
                    # More than one match found. Can only happen if search is
                    # done by name.
                    if result["numberReturned"] > 1:
                        self.warncell_name += " (not unique used ID)!"

                    self.__query = {
                        "typeName": weather_warnings_query_mapping[region]
                    }
                    # Special handling for counties
                    if region == "dwd:Warngebiete_Kreise":
                        self.__query[
                            "CQL_FILTER"
                        ] = f"GC_WARNCELLID='{self.warncell_id}'"
                    else:
                        self.__query[
                            "CQL_FILTER"
                        ] = f"WARNCELLID='{self.warncell_id}'"
                    break

    def __parse_result(self, json_obj):
        """Parse the retrieved data."""
        try:
            current_maxlevel = 0
            expected_maxlevel = 0
            current_warnings = []
            expected_warnings = []

            if json_obj["timeStamp"]:
                try:
                    self.last_update = ciso8601.parse_datetime(
                        json_obj["timeStamp"]
                    )
                except:  # pylint: disable=bare-except # noqa: E722
                    self.last_update = datetime.datetime.now(
                        datetime.timezone.utc
                    )
            else:
                self.last_update = datetime.datetime.now(datetime.timezone.utc)

            if json_obj["numberReturned"]:
                for feature in json_obj["features"]:
                    warning = convert_warning_data(feature["properties"])

                    current_time = datetime.datetime.now(datetime.timezone.utc)
                    # pylint: disable=bad-continuation
                    if (
                        warning["end_time"] is not None
                        and current_time > warning["end_time"]
                    ):
                        continue

                    if (
                        warning["start_time"] is not None
                        and warning["start_time"] < current_time
                    ):
                        current_warnings.append(warning)
                        current_maxlevel = max(
                            warning["level"], current_maxlevel
                        )
                    else:
                        expected_warnings.append(warning)
                        expected_maxlevel = max(
                            warning["level"], expected_maxlevel
                        )
                    # pylint: enable=bad-continuation

            self.current_warning_level = current_maxlevel
            self.current_warnings = current_warnings

            self.expected_warning_level = expected_maxlevel
            self.expected_warnings = expected_warnings
            self.data_valid = True

        except:  # pylint: disable=bare-except # noqa: E722
            self.data_valid = False
            self.last_update = None
            self.current_warning_level = None
            self.current_warnings = None
            self.expected_warning_level = None
            self.expected_warnings = None
