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
from typing import Tuple

import pytest

from pysolorie import (
    AtmosphericTransmission,
    HottelModel,
    IrradiationCalculator,
    Observer,
    SolarIrradiance,
    SunPosition,
)


@pytest.mark.parametrize(
    "climate_type, observer_altitude, expected_result",
    [
        ("MIDLATITUDE SUMMER", 1200, (0.228, 0.666, 0.309)),  # Tehran Summer
        ("MIDLATITUDE WINTER", 1200, (0.242, 0.679, 0.303)),  # Tehran Winter
        ("TROPICAL", 26, (0.124, 0.739, 0.392)),  # Medan
        ("SUBARCTIC SUMMER", 136, (0.140, 0.739, 0.379)),  # Fairbanks
    ],
)
def test_calculate_transmittance_components(
    climate_type: str,
    observer_altitude: int,
    expected_result: Tuple[float, float, float],
) -> None:
    hottel_model: HottelModel = HottelModel()
    result: Tuple[
        float, float, float
    ] = hottel_model.calculate_transmittance_components(climate_type, observer_altitude)
    assert pytest.approx(result, abs=1e-3) == expected_result


def test_invalid_climate_type() -> None:
    with pytest.raises(ValueError, match="Invalid climate type"):
        hottel_model: HottelModel = HottelModel()
        hottel_model.calculate_transmittance_components("INVALID", 1000)


@pytest.mark.parametrize(
    "day_of_year, solar_time, expected_declination, expected_hour_angle",
    [
        (1, 12 * 60 * 60, -0.4014257279586958, 0),  # January 1st at noon
        (81, 10 * 60 * 60, 0, -math.pi / 6),  # March 22nd at 10am (equinox)
        (81, 12 * 60 * 60, 0, 0),  # March 22nd at noon (equinox)
        (1, 13 * 60 * 60, -0.4014257279586958, math.pi / 12),  # January 1st at 1pm
    ],
)
def test_sun_position(
    day_of_year: int,
    solar_time: int,
    expected_declination: float,
    expected_hour_angle: float,
) -> None:
    sun_position: SunPosition = SunPosition()
    declination: float = sun_position.solar_declination(day_of_year)
    hour_angle: float = sun_position.hour_angle(solar_time)
    assert declination == pytest.approx(expected_declination, abs=1e-3)
    assert hour_angle == pytest.approx(expected_hour_angle, abs=1e-3)


@pytest.mark.parametrize(
    "hour_angle, expected_solar_time",
    [
        (0, 12 * 60 * 60),  # solar noon
        (-math.pi / 6, 10 * 60 * 60),  # 10am
        (math.pi / 12, 13 * 60 * 60),  # 1pm
    ],
)
def test_solar_time(
    hour_angle: float,
    expected_solar_time: int,
) -> None:
    sun_position: SunPosition = SunPosition()
    solar_time: float = sun_position.solar_time(hour_angle)
    assert solar_time == pytest.approx(expected_solar_time, abs=1e-3)


@pytest.mark.parametrize(
    "day_of_year, expected_irradiance",
    [
        (1, 1412.104),  # January 1st
        (81, 1374.918),  # March 22nd (equinox)
        (172, 1322.623),  # June 21st (summer solstice)
        (264, 1359.464),  # September 23rd (equinox)
        (355, 1411.444),  # December 21st (winter solstice)
    ],
)
def test_calculate_extraterrestrial_irradiance(
    day_of_year: int, expected_irradiance: float
) -> None:
    sun_position = SunPosition()
    solar_irradiance = SolarIrradiance(sun_position)
    irradiance: float = solar_irradiance.calculate_extraterrestrial_irradiance(
        day_of_year
    )
    assert irradiance == pytest.approx(expected_irradiance, abs=1e-3)


@pytest.mark.parametrize(
    "observer_latitude, observer_longitude, day_of_year, solar_time, expected_zenith_angle",
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
        (90, 0, 1, 13 * 60 * 60, 1.972),  # Test at North Pole on January 1st at 1pm
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
    zenith_angle: float = observer.calculate_zenith_angle(day_of_year, solar_time)
    assert zenith_angle == pytest.approx(expected_zenith_angle, abs=1e-3)


def test_calculate_zenith_angle_without_latitude():
    observer = Observer(None, 0)
    with pytest.raises(
        ValueError,
        match="Observer latitude must be provided.",
    ):
        observer.calculate_zenith_angle(1, 12 * 60 * 60)


@pytest.mark.parametrize(
    "climate_type, observer_altitude, observer_latitude, day_of_year, solar_time, expected_transmittance",
    [
        ("MIDLATITUDE SUMMER", 1200, 35.69, 81, 12 * 60 * 60, 0.683),  # Tehran Summer
        ("MIDLATITUDE WINTER", 1200, 35.69, 355, 12 * 60 * 60, 0.618),  # Tehran Winter
        ("TROPICAL", 63, 3.59, 81, 10 * 60 * 60, 0.597),  # Medan
        ("SUBARCTIC SUMMER", 136, 64.84, 1, 13 * 60 * 60, 0.140),  # Fairbanks
    ],
)
def test_calculate_transmittance(
    climate_type: str,
    observer_altitude: int,
    observer_latitude: float,
    day_of_year: int,
    solar_time: float,
    expected_transmittance: float,
) -> None:
    atmospheric_transmission: AtmosphericTransmission = AtmosphericTransmission(
        climate_type, observer_altitude, observer_latitude
    )
    result: float = atmospheric_transmission.calculate_transmittance(
        day_of_year, solar_time
    )
    assert pytest.approx(result, abs=1e-3) == expected_transmittance


@pytest.mark.parametrize(
    "day_of_year, expected_sunrise_hour_angle, expected_sunset_hour_angle",
    [
        (1, -1.261, 1.261),  # January 1st
        (81, -math.pi / 2, math.pi / 2),  # March 22nd (equinox)
        (172, -1.888, 1.888),  # June 21st (solstice)
    ],
)
def test_calculate_sunrise_sunset(
    day_of_year: int,
    expected_sunrise_hour_angle: float,
    expected_sunset_hour_angle: float,
) -> None:
    observer: Observer = Observer(observer_latitude=35.69)  # Tehran
    sunrise_hour_angle, sunset_hour_angle = observer.calculate_sunrise_sunset(
        day_of_year
    )
    assert sunrise_hour_angle == pytest.approx(expected_sunrise_hour_angle, abs=1e-3)
    assert sunset_hour_angle == pytest.approx(expected_sunset_hour_angle, abs=1e-3)


@pytest.mark.parametrize(
    "climate_type, observer_altitude, observer_latitude, day_of_year, expected_result",
    [
        (
            "MIDLATITUDE SUMMER",
            1200,
            35.6892,
            172,
            0.004,
        ),  # Tehran Summer, day_of_year=172 (June 21)
        (
            "MIDLATITUDE WINTER",
            1200,
            35.6892,
            355,
            1.114,
        ),  # Tehran Winter, day_of_year=355 (Dec 21)
        (
            "TROPICAL",
            26,
            3.5952,
            100,
            -0.116,
        ),  # Medan, day_of_year=100 (April 10)
        (
            "SUBARCTIC SUMMER",
            132,
            64.84361,
            200,
            0.569,
        ),  # Fairbanks Summer, day_of_year=200 (July 19)
    ],
)
def test_find_optimal_orientation(
    climate_type: str,
    observer_altitude: int,
    observer_latitude: float,
    day_of_year: int,
    expected_result: float,
) -> None:
    irradiation_calculator = IrradiationCalculator(
        climate_type, observer_altitude, observer_latitude
    )
    result = irradiation_calculator.find_optimal_orientation(day_of_year)
    assert pytest.approx(result, abs=1e-3) == expected_result
