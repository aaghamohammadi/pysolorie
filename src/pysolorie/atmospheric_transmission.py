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

from .model import HottelModel
from .observer import Observer


class AtmosphericTransmission:
    def __init__(
        self,
        climate_type: str,
        observer_altitude: int,
        observer_latitude: float,
    ):
        r"""
        To instantiate the ``AtmosphericTransmission`` class,
        provide the following three parameters.


        :param climate_type: The type of climate.
        :type climate_type: str
        :param observer_altitude: The altitude of the observer in meters.
        :type observer_altitude: int
        :param observer_latitude: The latitude of the observer in degrees.
        :type observer_latitude: float
        """
        self.hottel_model = HottelModel()
        (
            self.a0,
            self.a1,
            self.k,
        ) = self.hottel_model.calculate_transmittance_components(
            climate_type, observer_altitude
        )
        self.observer = Observer(observer_latitude)

    def calculate_transmittance(self, day_of_year: int, solar_time: float) -> float:
        r"""
        Calculate the effective atmospheric transmission coefficient of the direct beam.

        The effective atmospheric transmission coefficient of the direct beam
        is calculated using the formula:

        .. math::
            \tau_b = a_0 + a_1 \times \exp\left(-\frac{k}{\cos(\theta_z)}\right)


        | - :math:`\tau_b` is the effective atmospheric transmission
            coefficient of the direct beam
        | - :math:`a_0`, :math:`a_1`, and :math:`k` are the components
            of clear-sky beam radiation transmittance
        | - :math:`\theta_z` is the zenith angle

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :param solar_time: The solar time in seconds.
        :type solar_time: float
        :return: The effective atmospheric transmission coefficient of the direct beam.
        :rtype: float
        """

        zenith_angle = self.observer.calculate_zenith_angle(day_of_year, solar_time)
        cos_zenith_angle = math.cos(zenith_angle)
        EPSILON = 1e-8  # Small constant to prevent division by zero
        if abs(cos_zenith_angle) < EPSILON:
            return self.a0
        else:
            return self.a0 + self.a1 * math.exp(-self.k / cos_zenith_angle)
