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

from pysolorie import HottelModel, SunPosition

hottel_model = HottelModel()


@pytest.mark.parametrize(
    "climate_type, observer_altitude, expected_result",
    [
        ("MIDLATITUDE SUMMER", 1200, (0.228, 0.666, 0.309)),  # Tehran Summer
        ("MIDLATITUDE WINTER", 1200, (0.242, 0.679, 0.303)),  # Tehran Winter
        ("TROPICAL", 63, (0.128, 0.737, 0.389)),  # Medan
        ("SUBARCTIC SUMMER", 136, (0.140, 0.739, 0.379)),  # Fairbanks
    ],
)
def test_calculate_transmittance_components(climate_type, observer_altitude, expected_result):
    result = hottel_model.calculate_transmittance_components(climate_type, observer_altitude)
    assert pytest.approx(result, abs=1e-3) == expected_result


def test_invalid_climate_type():
    with pytest.raises(ValueError, match="Invalid climate type"):
        hottel_model.calculate_transmittance_components("INVALID", 1000)


@pytest.mark.parametrize(
    "day_of_year, solar_time, expected_declination, expected_hour_angle",
    [
        (1, 12, -0.4014257279586958, 0),  # January 1st at noon
        (81, 10, 0, -30),  # March 22nd at 2pm (equinox)
        (81, 12, 0, 0),  # March 22nd at noon (equinox)
        (1, 13, -0.4014257279586958, 15),  # January 1st at 1pm
    ],
)
def test_sun_position(day_of_year, solar_time, expected_declination, expected_hour_angle):
    sun_position = SunPosition(day_of_year, solar_time)
    declination = sun_position.solar_declination
    hour_angle = sun_position.hour_angle
    assert declination == pytest.approx(expected_declination, abs=1e-3)
    assert hour_angle == expected_hour_angle
