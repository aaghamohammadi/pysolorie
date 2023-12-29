#    Copyright 2023 Alireza Aghamohammadi

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import math

import pytest

from pysolorie import Observer


@pytest.mark.parametrize(
    "observer_latitude,"
    + "observer_longitude,"
    + "day_of_year,"
    + "solar_time,"
    + "expected_zenith_angle",
    [
        (
            35.69,
            51.39,
            81,
            12 * 60 * 60,
            0.623,
        ),  # Test at Tehran on the 81st day of the year at noon
        (
            35.69,
            51.39,
            355,
            12 * 60 * 60,
            1.032,
        ),  # Test at Tehran on the 355th day of the year at noon
        (
            3.59,
            98.67,
            81,
            10 * 60 * 60,
            0.527,
        ),  # Test at Medan on the 81st day of the year at 10am
        (
            64.84,
            -147.72,
            1,
            13 * 60 * 60,
            1.547,
        ),  # Test at Fairbanks on the 1st day of the year at 1pm
    ],
)
def test_calculate_zenith_angle(
    observer_latitude: float,
    observer_longitude: float,
    day_of_year: int,
    solar_time: int,
    expected_zenith_angle: float,
) -> None:
    observer: Observer = Observer(observer_latitude, observer_longitude)
    expected_observer_latitude = math.radians(observer_latitude)
    expected_observer_longitude = math.radians(observer_longitude)

    assert observer.observer_latitude == pytest.approx(
        expected_observer_latitude, abs=1e-3
    )
    assert observer.observer_longitude == pytest.approx(
        expected_observer_longitude, abs=1e-3
    )

    zenith_angle: float = observer.calculate_zenith_angle(day_of_year, solar_time)
    assert zenith_angle == pytest.approx(expected_zenith_angle, abs=1e-3)


def test_calculate_zenith_angle_without_latitude():
    observer = Observer(None, 0)
    with pytest.raises(
        ValueError,
        match="Missing required data: Observer latitude",
    ):
        observer.calculate_zenith_angle(1, 12 * 60 * 60)


@pytest.mark.parametrize(
    "observer_latitude,"
    + "day_of_year,"
    + "expected_sunrise_hour_angle,"
    + "expected_sunset_hour_angle",
    [
        (35.69, 1, -1.261, 1.261),  # January 1st, Tehran
        (35.69, 81, -math.pi / 2, math.pi / 2),  # March 22nd (equinox), Tehran
        (35.69, 172, -1.888, 1.888),  # June 21st (solstice), Tehran
        (70.00, 1, 0, 0),  # January 1st, Finnmark
        (70.00, 81, -math.pi / 2, math.pi / 2),  # March 22nd (equinox), Finnmark
        (70.00, 172, -math.pi, math.pi),  # June 21st (solstice), Finnmark
    ],
)
def test_calculate_sunrise_sunset(
    observer_latitude: float,
    day_of_year: int,
    expected_sunrise_hour_angle: float,
    expected_sunset_hour_angle: float,
) -> None:
    observer: Observer = Observer(observer_latitude=observer_latitude)
    sunrise_hour_angle, sunset_hour_angle = observer.calculate_sunrise_sunset(
        day_of_year
    )
    assert sunrise_hour_angle == pytest.approx(expected_sunrise_hour_angle, abs=1e-3)
    assert sunset_hour_angle == pytest.approx(expected_sunset_hour_angle, abs=1e-3)


def test_calculate_sunrise_sunset_invalid_latitude():
    invalid_latitudes = [89, -89]
    for invalid_latitude in invalid_latitudes:
        observer = Observer(invalid_latitude)
        with pytest.raises(
            ValueError,
            match="Invalid data: Observer latitude. ",
        ):
            observer.calculate_sunrise_sunset(day_of_year=172)
