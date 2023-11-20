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


class SunPosition:
    def __init__(self, day_of_year: int, solar_time: float):
        """
        Initialize the SunPosition class.

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :param solar_time: The solar time in hours.
        :type solar_time: float
        """
        self.day_of_year = day_of_year
        self.solar_time = solar_time

    @property
    def solar_declination(self) -> float:
        r"""
        Calculate the solar declination angle in radians.

        The solar declination angle is the angle between the rays of the sun and the plane of the Earth's equator.

        Formula:
        \[
        \delta = 23.45 * \sin \left( \frac{2 \pi}{365} * (284 + n) \right)
        \]

        :return: The solar declination angle in radians.
        :rtype: float
        """
        # Maximum tilt of the Earth's axis (in degrees)
        max_earth_tilt_degrees = 23.45

        # Convert the tilt to radians
        max_earth_tilt_radians = math.radians(max_earth_tilt_degrees)

        # Offset to ensure declination angle is zero at the March equinox
        equinox_offset_days = 284

        # Calculate the solar declination angle
        solar_declination = max_earth_tilt_radians * math.sin(
            (2 * math.pi) * (equinox_offset_days + self.day_of_year) / 365
        )

        return solar_declination

    @property
    def hour_angle(self) -> float:
        r"""
        Calculate the hour angle based on the solar time.

        The hour angle is a measure of time, expressed in angular terms, from solar noon.

        Formula:
        \[
        \omega = (t - 12) * 15
        \]

        :return: The hour angle in degrees.
        :rtype: float
        """
        # The Earth rotates by 15 degrees per hour
        earth_rotation_rate = 15

        # Calculate the hour angle
        hour_angle = (self.solar_time - 12) * earth_rotation_rate

        return hour_angle
