"""Python client to retrieve pollen flight forecast from DWD."""

from datetime import UTC, datetime

from .core import query_dwd


def convert_forecast_data(data_in):
    """Convert the data received from DWD."""
    try:
        data_out = {}
        data_out["start_time"] = datetime.fromisoformat(data_in["FORECAST_DATE"])
        data_out["level"] = data_in["POLLENINT"]
        data_out["impact"] = data_in["PARAMETER_VALUE"]
        try:
            colors = data_in["EC_AREA_COLOR"].split(" ")
            data_out["color"] = f"#{int(colors[0]):02x}{int(colors[1]):02x}"
            data_out["color"] += f"{int(colors[2]):02x}"
        except:  # pylint: disable=bare-except
            data_out["color"] = "#000000"
        return data_out
    except:  # pylint: disable=bare-except
        return None


class DwdPollenFlightAPI:
    """
    Class for retrieving the pollen flight forecast from DWD.

    Attributes:
    -----------
    data_valid : bool
        a flag wether or not the other attributes contain valid values
    cell_id : int
        the id of the selected cell
    cell_name : str
        the name of the selected cell
    last_update : datetime
        the timestamp of the last update
    forecast_data : dict
        dictionary containing the retrieved data
        key : int
            data type
        name : str
            string representation of the data type
        forecast : list
            list containing the forecast data
            start_time : datetime
                timestamp when the warning starts
            level : int
                impact level (0 - 6)
            impact : str
                string representation of the impact level
            color : str
                forecast color formatted #rrggbb
    """

    def __init__(self, identifier):
        """
        Init DWD pollen flight forecast.

        Parameters
        ----------
        identifier : str or int
            a valid cell id or name
            https://github.com/stephan192/dwdwfsapi/blob/master/docs/
            pollencells.md
        """
        self.data_valid = False
        self.cell_id = None
        self.cell_name = None
        self.__query = None
        self.last_update = None
        self.forecast_data = None

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
        length = 0
        if self.data_valid and self.forecast_data is not None:
            for data in self.forecast_data:
                length += len(self.forecast_data[data]["forecast"])
        return length

    def __str__(self):
        """Return a short overview about the actual status."""
        if self.data_valid and self.forecast_data is not None:
            highest_impact = 0
            for data in self.forecast_data:
                for forecast in self.forecast_data[data]["forecast"]:
                    if forecast["level"] > highest_impact:
                        highest_impact = forecast["level"]
            retval = f"Highest forecasted impact level: {highest_impact}"
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
            self.forecast_data = None

    def __generate_query(self, identifier):
        """Determine the id to which the identifier belongs."""
        region_query = {}
        # Numbers represent cell ids
        if isinstance(identifier, int) or identifier.isnumeric():
            region_query["CQL_FILTER"] = f"GF='{identifier}'"
        else:
            region_query["CQL_FILTER"] = f"GEN LIKE '%{identifier}%'"

        region_query["typeName"] = "dwd:Pollenfluggebiete"
        result = query_dwd(**region_query)
        if result is not None:
            if result["numberReturned"] > 0:
                self.cell_id = result["features"][0]["properties"]["GF"]
                self.cell_name = result["features"][0]["properties"]["GEN"]
                # More than one match found.
                # Workaround because DWD is returning some datasets twice
                not_unique = ""
                if result["numberReturned"] > 1:
                    for entry in result["features"]:
                        if entry["properties"]["GF"] != self.cell_id:
                            not_unique = " (not unique use ID!)"
                self.cell_name += not_unique

                self.__query = {"typeName": "dwd:Pollenflug"}
                self.__query["CQL_FILTER"] = f"GF='{self.cell_id}'"

    def __parse_result(self, json_obj):
        """Parse the retrieved data."""
        try:
            forecast_data = {}
            if json_obj["timeStamp"]:
                try:
                    self.last_update = datetime.fromisoformat(json_obj["timeStamp"])
                except:  # pylint: disable=bare-except
                    self.last_update = datetime.now(UTC)
            else:
                self.last_update = datetime.now(UTC)

            if json_obj["numberReturned"]:
                for feature in json_obj["features"]:
                    forecast = feature["properties"]

                    if not forecast["EC_II"] in forecast_data:
                        forecast_data[forecast["EC_II"]] = {}
                        forecast_data[forecast["EC_II"]]["name"] = forecast[
                            "PARAMETER_NAME"
                        ]
                        forecast_data[forecast["EC_II"]]["forecast"] = []

                    single_forecast = convert_forecast_data(forecast)
                    if (
                        single_forecast is not None
                        and single_forecast
                        not in forecast_data[forecast["EC_II"]]["forecast"]
                    ):
                        forecast_data[forecast["EC_II"]]["forecast"].append(
                            single_forecast
                        )

            # Sort list of forecast entries by start_time
            for data in forecast_data.values():
                data["forecast"].sort(key=lambda k: k["start_time"])

            self.forecast_data = forecast_data
            self.data_valid = True

        except:  # pylint: disable=bare-except
            self.data_valid = False
            self.last_update = None
            self.forecast_data = None
