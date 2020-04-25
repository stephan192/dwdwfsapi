# -*- coding: utf-8 -*-
"""Tests for dwdwfsapi weatherwarnings module."""

import datetime
from dwdwfsapi import DwdWeatherWarningsAPI

MIN_WARNING_LEVEL = 0  # 0 = no warning
MAX_WARNING_LEVEL = 4  # 4 = extreme weather
TIME_TOLERANCE = 5  # seconds

WARNCELL_ID_CITY = 808436003
WARNCELL_NAME_CITY = "Gemeinde Aichstetten"
WARNCELL_ID_COUNTY = 106439000
WARNCELL_NAME_COUNTY = "Rheingau-Taunus-Kreis"
WARNCELL_ID_LAKE = 209903000
WARNCELL_NAME_LAKE = "Forggensee"
WARNCELL_ID_COAST = 501000002
WARNCELL_NAME_COAST = "Helgoland"
WARNCELL_ID_SEA = 401000010
WARNCELL_NAME_SEA = "Utsira"


def test_city():
    """Test a city warncell."""
    dwd = DwdWeatherWarningsAPI(WARNCELL_ID_CITY)
    assert dwd.data_valid
    assert dwd.warncell_id == WARNCELL_ID_CITY
    assert dwd.warncell_name == WARNCELL_NAME_CITY
    start_time = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(0, TIME_TOLERANCE)
    stop_time = start_time + datetime.timedelta(0, (2 * TIME_TOLERANCE))
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


def test_county():
    """Test a county warncell."""
    dwd = DwdWeatherWarningsAPI(WARNCELL_NAME_COUNTY)
    assert dwd.data_valid
    assert dwd.warncell_id == WARNCELL_ID_COUNTY
    assert dwd.warncell_name == WARNCELL_NAME_COUNTY
    start_time = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(0, TIME_TOLERANCE)
    stop_time = start_time + datetime.timedelta(0, (2 * TIME_TOLERANCE))
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


def test_lake():
    """Test a lake warncell."""
    dwd = DwdWeatherWarningsAPI(WARNCELL_ID_LAKE)
    assert dwd.data_valid
    assert dwd.warncell_id == WARNCELL_ID_LAKE
    assert dwd.warncell_name == WARNCELL_NAME_LAKE
    start_time = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(0, TIME_TOLERANCE)
    stop_time = start_time + datetime.timedelta(0, (2 * TIME_TOLERANCE))
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


def test_coast():
    """Test a coast warncell."""
    dwd = DwdWeatherWarningsAPI(WARNCELL_NAME_COAST)
    assert dwd.data_valid
    assert dwd.warncell_id == WARNCELL_ID_COAST
    assert dwd.warncell_name == WARNCELL_NAME_COAST
    start_time = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(0, TIME_TOLERANCE)
    stop_time = start_time + datetime.timedelta(0, (2 * TIME_TOLERANCE))
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


def test_sea():
    """Test a sea warncell."""
    dwd = DwdWeatherWarningsAPI(WARNCELL_ID_SEA)
    assert dwd.data_valid
    assert dwd.warncell_id == WARNCELL_ID_SEA
    assert dwd.warncell_name == WARNCELL_NAME_SEA
    start_time = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(0, TIME_TOLERANCE)
    stop_time = start_time + datetime.timedelta(0, (2 * TIME_TOLERANCE))
    assert start_time < dwd.last_update < stop_time
    assert MIN_WARNING_LEVEL <= dwd.current_warning_level <= MAX_WARNING_LEVEL
    assert MIN_WARNING_LEVEL <= dwd.expected_warning_level <= MAX_WARNING_LEVEL
    assert isinstance(dwd.current_warnings, list)
    assert isinstance(dwd.expected_warnings, list)


def test_wrong_input():
    """Test an invalid input."""
    dwd = DwdWeatherWarningsAPI(None)
    assert not dwd.data_valid
    assert dwd.warncell_id is None
    assert dwd.warncell_name is None
    assert dwd.last_update is None
    assert dwd.current_warning_level is None
    assert dwd.expected_warning_level is None
    assert dwd.current_warnings is None
    assert dwd.expected_warnings is None
