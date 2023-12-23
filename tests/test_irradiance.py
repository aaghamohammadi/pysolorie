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

from pysolorie import SolarIrradiance, SunPosition


@pytest.mark.parametrize(
    "day_of_year, expected_irradiance",
    [
        (1, 0.001411444),  # January 1st
        (81, 0.001374918),  # March 22nd (equinox)
        (172, 0.00132262),  # June 21st (summer solstice)
        (264, 0.001359464),  # September 23rd (equinox)
        (355, 0.001412104),  # December 21st (winter solstice)
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
    assert irradiance == pytest.approx(expected_irradiance, abs=1e-5)
