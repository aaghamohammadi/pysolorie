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

from .exceptions import MissingObserverLatitudeError
from .sun_position import SunPosition


class Observer:
    r"""
    A class to model an observer based on horizontal and equatorial pictures
    of the sun-earth geometry.
    """

    def __init__(
        self,
        observer_latitude: Optional[float] = None,
        observer_longitude: Optional[float] = None,
    ):
        """
        To instantiate the ``Observer`` class, provide the following parameter.

        :param observer_latitude: The latitude of the observer in degrees (optional).
        :type observer_latitude: Optional[float]
        :param observer_longitude: The longitude of the observer in degrees (optional).
        :type observer_longitude: Optional[float]
        """
        self.observer_latitude = observer_latitude
        self.observer_longitude = observer_longitude
        self.sun_position = SunPosition()

    def calculate_zenith_angle(self, day_of_year: int, solar_time: float) -> float:
        r"""
        Calculate the solar zenith angle.

        The solar zenith angle is calculated using the formula:

        .. math::
            \cos(\theta_z) = \sin(\phi) \times \sin(\delta)
            + \cos(\phi) \times \cos(\delta) \times \cos(\omega)


        | - :math:`\theta_z` is the solar zenith angle
        | - :math:`\phi` is the latitude of the observer
        | - :math:`\delta` is the solar declination
        | - :math:`\omega` is the hour angle.

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :param solar_time: The solar time in seconds.
        :type solar_time: float
        :return: The zenith angle in radians.
        :rtype: float
        """
        observer_latitude = self._ensure_latitude_provided()

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
            \cos(\omega) = -\tan(\phi) \times \tan(\delta)


        | - :math:`\omega` is the hour angle
        | - :math:`\phi` is the latitude of the observer
        | - :math:`\delta` is the solar declination.

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :return: The hour angle at sunrise and sunset in radians.
        :rtype: tuple
        """
        observer_latitude = self._ensure_latitude_provided()

        solar_declination = self.sun_position.solar_declination(day_of_year)
        hour_angle = math.acos(
            -math.tan(observer_latitude) * math.tan(solar_declination)
        )

        sunrise = -hour_angle
        sunset = hour_angle

        return sunrise, sunset

    def _ensure_latitude_provided(self) -> float:
        if self.observer_latitude is None:
            raise MissingObserverLatitudeError()
        return self.observer_latitude

    _observer_latitude: Optional[float]

    @property
    def observer_latitude(self) -> Optional[float]:
        """
        Getter for the observer's latitude.

        :return: The observer's latitude in radians.
        :rtype: Optional[float]
        """
        return self._observer_latitude

    @observer_latitude.setter
    def observer_latitude(self, value: Optional[float]):
        """
        Setter for the observer's latitude. Converts the value to radians if not None.

        :param value: The observer's latitude in degrees.
        :type value: Optional[float]
        """
        self._observer_latitude = math.radians(value) if value is not None else None

    _observer_longitude: Optional[float]

    @property
    def observer_longitude(self) -> Optional[float]:
        """
        Getter for the observer's longitude.

        :return: The observer's longitude in radians.
        :rtype: Optional[float]
        """
        return self._observer_longitude

    @observer_longitude.setter
    def observer_longitude(self, value: Optional[float]):
        """
        Setter for the observer's longitude. Converts the value to radians if not None.

        :param value: The observer's longitude in degrees.
        :type value: Optional[float]
        """
        self._observer_longitude = math.radians(value) if value is not None else None
