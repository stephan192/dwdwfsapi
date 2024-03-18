"""Tests for dwdwfsapi weatherwarnings module."""

from datetime import UTC, datetime, timedelta

import pytest

from dwdwfsapi import DwdWeatherWarningsAPI

MIN_WARNING_LEVEL = 0  # 0 = no warning
MAX_WARNING_LEVEL = 4  # 4 = extreme weather
TIME_TOLERANCE = 15  # seconds

testdata_ident = [
    (808436003, "Gemeinde Aichstetten"),
    (106439000, "Rheingau-Taunus-Kreis"),
    (209903000, "Forggensee"),
    (501000002, "Helgoland"),
]

testdata_name = [
    ("Gemeinde Olching", 809179142),
    ("Kreis Stade", 103359000),
    ("Wörthsee", 209906000),
    ("Östlich Rügen", 501000008),
]

testdata_gps = [
    ((53.34108422289897, 7.1901377643426745), 803402000, "Stadt Emden"),
    ((51.34854410136008, 12.371143867332414), 714713005, "Leipzig-Mitte"),
]

testdata_invalid = [12345678, "Hintertupfing", (0.0, 0.0)]


@pytest.mark.parametrize("ident, name", testdata_ident)
def test_id(ident, name):
    """Test a given warncell id."""
    start_time = datetime.now(UTC) - timedelta(seconds=TIME_TOLERANCE)
    stop_time = datetime.now(UTC) + timedelta(seconds=TIME_TOLERANCE)
    dwd = DwdWeatherWarningsAPI(ident)

    assert dwd.data_valid
    assert dwd.warncell_id == ident
    assert dwd.warncell_name == name
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


@pytest.mark.parametrize("name, ident", testdata_name)
def test_name(name, ident):
    """Test a given warncell name."""
    start_time = datetime.now(UTC) - timedelta(seconds=TIME_TOLERANCE)
    stop_time = datetime.now(UTC) + timedelta(seconds=TIME_TOLERANCE)
    dwd = DwdWeatherWarningsAPI(ident)

    assert dwd.data_valid
    assert dwd.warncell_id == ident
    assert dwd.warncell_name == name
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


@pytest.mark.parametrize("location, ident, name", testdata_gps)
def test_gps_location(location, ident, name):
    """Test determining the warncell through gps."""
    start_time = datetime.now(UTC) - timedelta(seconds=TIME_TOLERANCE)
    stop_time = datetime.now(UTC) + timedelta(seconds=TIME_TOLERANCE)
    dwd = DwdWeatherWarningsAPI(location)

    assert dwd.data_valid
    assert dwd.warncell_id == ident
    assert dwd.warncell_name == name
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


@pytest.mark.parametrize("ident_name_gps", testdata_invalid)
def test_wrong_input(ident_name_gps):
    """Test an invalid input."""
    dwd = DwdWeatherWarningsAPI(ident_name_gps)

    assert not dwd.data_valid
    assert dwd.warncell_id is None
    assert dwd.warncell_name is None
    assert dwd.last_update is None
    assert dwd.current_warning_level is None
    assert dwd.expected_warning_level is None
    assert dwd.current_warnings is None
    assert dwd.expected_warnings is None
