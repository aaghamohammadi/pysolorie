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
    r"""
    A class to model the solar irradiance.
    """

    def __init__(self, sun_position: SunPosition):
        r"""
        To instantiate the ``SolarIrradiance`` class, provide the following parameter.


        :param sun_position: An instance of the SunPosition class.
        :type sun_position: pysolorie.SunPosition
        """
        self.sun_position = sun_position

    def calculate_extraterrestrial_irradiance(self, day_of_year: int) -> float:
        r"""
        Calculate the extraterrestrial solar irradiance for a given day of the year.

        The extraterrestrial solar irradiance, :math:`I`,
        is the annual average of the Sun's irradiation intensity.
        This refers to the amount of solar energy received per unit
        area per unit time on a surface perpendicular to the Sun's rays,
        outside Earth's atmosphere.

        The formula used is:

        .. math::
            I(n) = SC
            \times (1 + 0.033 \times \cos (\frac{2\pi~n}{365}))


        | - :math:`SC` is the average solar radiation arriving outside
           of the Earth's atmosphere,
           which is approximately ``1367`` Megawatts per square meter [1]_.
           This is also known as the solar constant.
        | - The factor ``0.033``, which is two times the eccentricity of
            the Earth's orbit around the Sun, accounts for the variation
            in the Earth-Sun distance due to the Earth's elliptical orbit.
        | - :math:`n` is the day of the year (i.e., ``day_of_year``)

        :param day\_of\_year: The day of the year, ranging from 1 to 365.
        :type day\_of\_year: int

        :return: The extraterrestrial solar irradiance in Megawatts per square meter.
        :rtype: float

        References
        ----------
        .. [1] Duffie (Deceased), J., Beckman, W., & Blair, N. (2020).
                Solar Engineering of Thermal Processes, Photovoltaics and Wind. Wiley.
        """

        # Solar constant (MW/m^2)
        SOLAR_CONSTANT = 1367 * 1e-6

        # Factor to account for the Earth's orbital eccentricity
        earth_orbital_eccentricity = 0.033

        # Calculate the extraterrestrial solar irradiance
        extraterrestrial_irradiance = SOLAR_CONSTANT * (
            1 + earth_orbital_eccentricity * math.cos(2 * math.pi * day_of_year / 365)
        )

        return extraterrestrial_irradiance
