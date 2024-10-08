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

import pytest

from pysolorie import IrradiationCalculator


@pytest.mark.parametrize(
    "climate_type,"
    + "observer_altitude,"
    + "observer_latitude,"
    + "day_of_year,"
    + "panel_orientation,"
    + "expected_result",
    [
        (
            "MIDLATITUDE SUMMER",
            1200,
            35.6892,
            172,
            45.0,
            19.961,  # Tehran Summer, day_of_year=172 (June 21)
        ),
        (
            "MIDLATITUDE WINTER",
            1200,
            35.6892,
            355,
            45.0,
            19.110,  # Tehran Winter, day_of_year=355 (Dec 21)
        ),
        (
            "TROPICAL",
            26,
            3.5952,
            100,
            45.0,
            13.003,  # Medan, day_of_year=100 (April 10)
        ),
        (
            "SUBARCTIC SUMMER",
            132,
            64.84361,
            200,
            45.0,
            21.012,  # Fairbanks Summer, day_of_year=200 (July 19)
        ),
        (
            "SUBARCTIC SUMMER",
            356,
            70.00,
            355,
            45.0,
            0,  # Finnmark Winter, day_of_year=355 (December 21)
        ),
    ],
)
def test_calculate_direct_irradiation(
    climate_type: str,
    observer_altitude: int,
    observer_latitude: float,
    day_of_year: int,
    panel_orientation: float,
    expected_result: float,
) -> None:
    irradiation_calculator = IrradiationCalculator(
        climate_type, observer_altitude, observer_latitude
    )
    result = irradiation_calculator.calculate_direct_irradiation(
        panel_orientation, day_of_year
    )
    assert pytest.approx(result, abs=1e-3) == expected_result


@pytest.mark.parametrize(
    "climate_type, observer_altitude, observer_latitude, day_of_year, expected_result",
    [
        (
            "MIDLATITUDE SUMMER",
            1200,
            35.6892,
            172,
            0.170,
        ),  # Tehran Summer, day_of_year=172 (June 21)
        (
            "MIDLATITUDE WINTER",
            1200,
            35.6892,
            355,
            63.791,
        ),  # Tehran Winter, day_of_year=355 (Dec 21)
        (
            "TROPICAL",
            26,
            3.5952,
            100,
            -6.610,
        ),  # Medan, day_of_year=100 (April 10)
        (
            "SUBARCTIC SUMMER",
            132,
            64.84361,
            200,
            32.614,
        ),  # Fairbanks Summer, day_of_year=200 (July 19)
        (
            "SUBARCTIC SUMMER",
            356,
            70.00,
            355,
            90,  # Finnmark Winter, day_of_year=355 (December 21)
        ),
        (
            "SUBARCTIC SUMMER",
            356,
            70.00,
            172,
            31.505,  # Finnmark Summer, day_of_year=172 (June 21)
        ),
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
