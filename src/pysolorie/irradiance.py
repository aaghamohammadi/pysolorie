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

from .sun_position import SunPosition


class SolarIrradiance:
    def __init__(self, sun_position: SunPosition):
        """
        Initialize the SolarIrradiance class.

        :param sun_position: An instance of the SunPosition class.
        :type sun_position: SunPosition
        """
        self.sun_position = sun_position

    def calculate_extraterrestrial_irradiance(self, day_of_year: int) -> float:
        r"""
        Calculate the extraterrestrial solar irradiance for a given day of the year.

        The extraterrestrial solar irradiance, E, is the amount of solar energy received
        per unit area on a surface perpendicular to the Sun's rays outside Earth's atmosphere.

        The formula used is:
        \[
        E = SOLAR_CONSTANT * (1 + 0.33 * cos (2 * pi * day_of_year / 365))
        \]

        where:
        - SOLAR_CONSTANT is the average solar radiation arriving outside of the Earth's atmosphere,
          which is approximately 1367 Watts per square meter. This is also known as the solar constant.
        - The factor 0.033 accounts for the variation in the Earth-Sun distance due to the Earth's elliptical orbit.

        :param day_of_year: The day of the year, ranging from 1 to 365.
        :type day_of_year: int

        :return: The extraterrestrial solar irradiance in Watts per square meter.
        :rtype: float
        """
        # Solar constant (W/m^2)
        SOLAR_CONSTANT = 1367

        # Factor to account for the Earth's orbital eccentricity
        earth_orbital_eccentricity = 0.033

        # Calculate the extraterrestrial solar irradiance
        extraterrestrial_irradiance = SOLAR_CONSTANT * (
            1 + earth_orbital_eccentricity * math.cos(2 * math.pi * day_of_year / 365)
        )

        return extraterrestrial_irradiance
