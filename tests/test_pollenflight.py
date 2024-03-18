"""Tests for dwdwfsapi pollenflight module."""

from datetime import UTC, datetime, timedelta

import pytest

from dwdwfsapi import DwdPollenFlightAPI

MIN_LEVEL = 0  # 0 = none
MAX_LEVEL = 6  # 3 = high
TIME_TOLERANCE = 15  # seconds
FORECAST_TYPES = 8  # Number of different forecast types
FORECAST_COUNT = 3  # Number forecasts per type

testdata_ident = [
    (11, "Inseln und Marschen"),
    (62, "Harz"),
    (122, "Donauniederungen"),
]

testdata_name = [
    ("Mecklenburg-Vorpommern", 20),
    ("Rhein-Main", 92),
    ("Hohenlohe/mittlerer Neckar/Oberschwaben", 112),
]

testdata_invalid = [130, "Hintertupfing"]


@pytest.mark.parametrize("ident, name", testdata_ident)
def test_id(ident, name):
    """Test a given cell id."""
    start_time = datetime.now(UTC) - timedelta(seconds=TIME_TOLERANCE)
    stop_time = datetime.now(UTC) + timedelta(seconds=TIME_TOLERANCE)
    dwd = DwdPollenFlightAPI(ident)

    assert dwd.data_valid
    assert dwd.cell_id == ident
    assert dwd.cell_name == name
    assert start_time < dwd.last_update < stop_time
    assert isinstance(dwd.forecast_data, dict)
    assert len(dwd.forecast_data) == FORECAST_TYPES
    for v in dwd.forecast_data.values():
        assert len(v["forecast"]) == FORECAST_COUNT
        for entry in v["forecast"]:
            assert MIN_LEVEL <= entry["level"] <= MAX_LEVEL


@pytest.mark.parametrize("name, ident", testdata_name)
def test_name(name, ident):
    """Test a given cell name."""
    start_time = datetime.now(UTC) - timedelta(seconds=TIME_TOLERANCE)
    stop_time = datetime.now(UTC) + timedelta(seconds=TIME_TOLERANCE)
    dwd = DwdPollenFlightAPI(ident)

    assert dwd.data_valid
    assert dwd.cell_id == ident
    assert dwd.cell_name == name
    assert start_time < dwd.last_update < stop_time
    assert isinstance(dwd.forecast_data, dict)
    assert len(dwd.forecast_data) == FORECAST_TYPES
    for v in dwd.forecast_data.values():
        assert len(v["forecast"]) == FORECAST_COUNT
        for entry in v["forecast"]:
            assert MIN_LEVEL <= entry["level"] <= MAX_LEVEL


@pytest.mark.parametrize("ident_name", testdata_invalid)
def test_wrong_input(ident_name):
    """Test an invalid input."""
    dwd = DwdPollenFlightAPI(ident_name)

    assert not dwd.data_valid
    assert dwd.cell_id is None
    assert dwd.cell_name is None
    assert dwd.last_update is None
    assert dwd.forecast_data is None
