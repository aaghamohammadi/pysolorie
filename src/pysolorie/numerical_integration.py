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
from typing import Tuple

import numpy as np
from scipy import integrate, optimize  # type: ignore

from .atmospheric_transmission import AtmosphericTransmission
from .irradiance import SolarIrradiance
from .observer import Observer
from .sun_position import SunPosition


class IrradiationCalculator:
    OMEGA = 7.15 * 1e-5

    def __init__(
        self, climate_type: str, observer_altitude: int, observer_latitude: float
    ):
        """
        Initialize the IrradiationCalculator class.

        :param climate_type: The type of climate.
        :type climate_type: str
        :param observer_altitude: The altitude of the observer in meters.
        :type observer_altitude: int
        :param observer_latitude: The latitude of the observer in degrees.
        :type observer_latitude: float
        """
        self._observer = Observer(observer_latitude=observer_latitude)
        self._sun_position = SunPosition()
        self._solar_irradiance = SolarIrradiance(self._sun_position)
        self._atmospheric_transmission = AtmosphericTransmission(
            climate_type, observer_altitude, observer_latitude
        )

    @staticmethod
    def _heaviside(x: float) -> int:
        """
        Heaviside step function.

        :param x: Input to the function.
        :type x: float
        :return: 1 if x >= 0, else 0.
        :rtype: int
        """
        return 1 if x >= 0 else 0

    def _calculate_irradiance_component(
        self, hour_angle: float, panel_orientation: float, day_of_year: int
    ) -> float:
        r"""
        Calculate a component of the irradiance integral.

        :param hour_angle: The hour angle.
        :type hour_angle: float
        :param panel_orientation: The orientation of the solar panel in radians.
        :type panel_orientation: float
        :param day_of_year: The day of the year.
        :type day_of_year: int
        :return: A component of the irradiance integral.
        :rtype: float
        """
        observer_latitude = self._observer._validate_latitude()
        solar_declination = self._sun_position.solar_declination(day_of_year)
        cos_theta = math.sin(solar_declination) * math.sin(
            observer_latitude - panel_orientation
        ) + math.cos(solar_declination) * math.cos(hour_angle) * math.cos(
            observer_latitude - panel_orientation
        )
        transmittance = self._atmospheric_transmission.calculate_transmittance(
            day_of_year, self._sun_position.solar_time(hour_angle)
        )
        irradiance = self._solar_irradiance.calculate_extraterrestrial_irradiance(
            day_of_year
        )
        return (
            irradiance
            * transmittance
            * cos_theta
            * self._heaviside(cos_theta)
            / self.OMEGA
        )

    def calculate_direct_irradiation(
        self, panel_orientation: float, day_of_year: int
    ) -> float:
        r"""
        Calculate the total direct irradiation for a given solar panel orientation (beta).

        The total direct irradiation is calculated using the formula:

        .. math::
            E_b(n,\phi) = \frac{E}{\Omega} \int_{\omega_s}^{\omega_t} \cos(θ) H(\cos(θ)) \times \tau_b  d\omega


        where:
         n is the day of year
         \(\phi\) is the latitude of the observer, and
         \(E\) is the amount of solar energy received
         \Omega is a constant equal to 7.15 * 1e-5
         theta is incidence angle
         \omega_s is the sunrise hour angle
         \omega_t is the sunset hour angle
         H is the heaviside step function


        :param panel_orientation: The orientation of the solar panel in radians.
        :type panel_orientation: float
        :param day_of_year: The day of the year.
        :type day_of_year: int
        :return: The total direct irradiation (negative because we want to maximize).
        :rtype: float
        """
        sunrise_hour_angle, sunset_hour_angle = self._observer.calculate_sunrise_sunset(
            day_of_year
        )
        irradiance_components = [
            self._calculate_irradiance_component(
                hour_angle, panel_orientation, day_of_year
            )
            for hour_angle in np.arange(sunrise_hour_angle, sunset_hour_angle, 0.01)
        ]
        return integrate.simpson(irradiance_components, dx=0.01)

    def find_optimal_orientation(self, day_of_year: int) -> float:
        """
        Find the optimal orientation (beta) that maximizes the total direct irradiation.

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :return: The optimal orientation (beta) in radians.
        :rtype: float
        """
        betas = np.arange(-math.pi / 2, math.pi / 2, 0.005)  # Discretize beta
        irradiations = [
            self.calculate_direct_irradiation(beta, day_of_year) for beta in betas
        ]
        optimal_beta = betas[
            np.argmax(irradiations)
        ]  # Find beta that gives max irradiation
        return optimal_beta