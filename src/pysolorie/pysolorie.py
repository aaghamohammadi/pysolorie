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

from typing import Dict, Tuple


class HottelModel:
    r"""
    Hottel Model for estimating clear-sky beam radiation transmittance
    based on climate type, and observer altitude.

    :ivar CLIMATE_CONSTANTS: Correction factors for different climate types (\(r_0\), \(r_1\), and \(r_k\)).
    """

    CLIMATE_CONSTANTS: Dict[str, Tuple[float, float, float]] = {
        "TROPICAL": (0.95, 0.98, 1.02),
        "MIDLATITUDE SUMMER": (0.97, 0.99, 1.02),
        "SUBARCTIC SUMMER": (0.99, 0.99, 1.01),
        "MIDLATITUDE WINTER": (1.03, 1.01, 1.00),
    }

    def _convert_to_km(self, observer_altitude: int) -> float:
        r"""
        Convert altitude from meters to kilometers.

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: Altitude in kilometers.
        :rtype: float
        """
        return observer_altitude / 1000.0

    def _calculate_a0_star(self, observer_altitude: int) -> float:
        r"""
        Calculate \(a_0^*\) based on observer altitude.

        Formula:
        \[
        a_0^* = 0.4237 - 0.00821 \cdot (6 - A)^2
        \]

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: \(a_0^*\) value.
        :rtype: float
        """
        observer_altitude_km = self._convert_to_km(observer_altitude)
        observer_altitude_diff = 6.0 - observer_altitude_km
        return 0.4237 - 0.00821 * observer_altitude_diff**2

    def _calculate_a1_star(self, observer_altitude: int) -> float:
        r"""
        Calculate \(a_1^*\) based on observer altitude.

        Formula:
        \[
        a_1^* = 0.5055 + 0.00595 \cdot (6.5 - A)^2
        \]

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: \(a_1^*\) value.
        :rtype: float
        """
        observer_altitude_km = self._convert_to_km(observer_altitude)
        observer_altitude_diff = 6.5 - observer_altitude_km
        return 0.5055 + 0.00595 * observer_altitude_diff**2

    def _calculate_k_star(self, observer_altitude: int) -> float:
        r"""
        Calculate \(k^*\) based on observer altitude.

        Formula:
        \[
        k^* = 0.2711 + 0.01858 \cdot (2.5 - A)^2
        \]

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: \(k^*\) value.
        :rtype: float
        """
        observer_altitude_km = self._convert_to_km(observer_altitude)
        observer_altitude_diff = 2.5 - observer_altitude_km
        return 0.2711 + 0.01858 * observer_altitude_diff**2

    def calculate_transmittance_components(
        self, climate_type: str, observer_altitude: int
    ) -> Tuple[float, float, float]:
        r"""
        Calculate the components of clear-sky beam radiation transmittance (\(a_0\), \(a_1\), and \(k\))
        based on climate type and observer altitude.

        Correction factors adjust the clear-sky beam radiation transmittance components.

        Formula:
        \[
        a_0 = r_0 \cdot a_0^*
        a_1 = r_1 \cdot a_1^*
        k = r_k \cdot k^*
        \]

        :param climate_type: Climate type (e.g., "TROPICAL").
        :type climate_type: str
        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: Components of clear-sky beam radiation transmittance (\(a_0\), \(a_1\), \(k\)).
        :rtype: tuple of floats
        :raises ValueError: If an invalid climate type is provided.
        """
        if climate_type.upper() not in self.CLIMATE_CONSTANTS:
            raise ValueError("Invalid climate type")

        r0, r1, rk = self.CLIMATE_CONSTANTS[climate_type.upper()]

        a0_star = self._calculate_a0_star(observer_altitude)
        a1_star = self._calculate_a1_star(observer_altitude)
        k_star = self._calculate_k_star(observer_altitude)

        a0 = r0 * a0_star
        a1 = r1 * a1_star
        k = rk * k_star

        return a0, a1, k
