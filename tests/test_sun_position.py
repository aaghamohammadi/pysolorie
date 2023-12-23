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

from pysolorie import SunPosition


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
        (math.pi, 24 * 60 * 60),  # solar night
    ],
)
def test_solar_time(
    hour_angle: float,
    expected_solar_time: int,
) -> None:
    sun_position: SunPosition = SunPosition()
    solar_time: float = sun_position.solar_time(hour_angle)
    assert solar_time == pytest.approx(expected_solar_time, abs=1e-3)
