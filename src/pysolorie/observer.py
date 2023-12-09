# Copyright 2023 Alireza Aghamohammadi

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from typing import Optional

from .sun_position import SunPosition


class Observer:
    def __init__(
        self,
        observer_latitude: Optional[float] = None,
        observer_longitude: Optional[float] = None,
    ):
        """
        Initialize the Observer class.

        :param observer_latitude: The latitude of the observer in degrees (optional).
        :type observer_latitude: Optional[float]
        :param observer_longitude: The longitude of the observer in degrees (optional).
        :type observer_longitude: Optional[float]
        """
        self.observer_latitude = (
            math.radians(observer_latitude) if observer_latitude is not None else None
        )
        self.observer_longitude = (
            math.radians(observer_longitude) if observer_longitude is not None else None
        )
        self.sun_position = SunPosition()

    def calculate_zenith_angle(self, day_of_year: int, solar_time: float) -> float:
        r"""
        Calculate the zenith angle.

        The zenith angle is calculated using the formula:

        .. math::
            \cos(\theta_z) = \sin(\phi) \cdot \sin(\delta)
            + \cos(\phi) \cdot \cos(\delta) \cdot \cos(\omega)

        where:
        \(\theta_z\) is the zenith angle,
        \(\phi\) is the latitude of the observer,
        \(\delta\) is the solar declination, and
        \(\omega\) is the hour angle.

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :param solar_time: The solar time in seconds.
        :type solar_time: float
        :return: The zenith angle in radians.
        :rtype: float
        """
        observer_latitude = self._validate_latitude()

        solar_declination = self.sun_position.solar_declination(day_of_year)
        hour_angle = self.sun_position.hour_angle(solar_time)
        return math.acos(
            math.sin(observer_latitude) * math.sin(solar_declination)
            + math.cos(observer_latitude)
            * math.cos(solar_declination)
            * math.cos(hour_angle)
        )

    def calculate_sunrise_sunset(self, day_of_year: int) -> tuple:
        r"""
        Calculate the hour angle at sunrise and sunset.

        The hour angle at sunrise and sunset is calculated using the formula:

        .. math::
            \cos(\omega) = -\tan(\phi) \cdot \tan(\delta)

        where:
        \(\omega\) is the hour angle,
        \(\phi\) is the latitude of the observer, and
        \(\delta\) is the solar declination.

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :return: The hour angle at sunrise and sunset in radians.
        :rtype: tuple
        """
        observer_latitude = self._validate_latitude()

        solar_declination = self.sun_position.solar_declination(day_of_year)
        hour_angle = math.acos(
            -math.tan(observer_latitude) * math.tan(solar_declination)
        )

        sunrise = -hour_angle
        sunset = hour_angle

        return sunrise, sunset

    def _validate_latitude(self) -> float:
        if self.observer_latitude is None:
            raise ValueError("Observer latitude must be provided.")
        return self.observer_latitude
