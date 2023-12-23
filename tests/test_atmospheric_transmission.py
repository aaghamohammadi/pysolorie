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

from pysolorie import AtmosphericTransmission


@pytest.mark.parametrize(
    "climate_type,"
    + "observer_altitude,"
    + "observer_latitude,"
    + "day_of_year,"
    + "solar_time,"
    + "expected_transmittance",
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
