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

    Climate Constants are Correction factors for different climate types
    :math:`r_0`, :math:`r_1`, and :math:`r_k`.

    .. list-table:: Climate Constants
       :widths: 25 25 25 25
       :header-rows: 1

       * - Climate Type
         - :math:`r_0`
         - :math:`r_1`
         - :math:`r_k`
       * - TROPICAL
         - 0.95
         - 0.98
         - 1.02
       * - MIDLATITUDE SUMMER
         - 0.97
         - 0.99
         - 1.02
       * - SUBARCTIC SUMMER
         - 0.99
         - 0.99
         - 1.01
       * - MIDLATITUDE WINTER
         - 1.03
         - 1.01
         - 1.00
    """

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
        Calculate :math:`a_0^*` based on observer altitude.

        The formula used to calculate :math:`a_0^*` is:

        .. math::
            a_0^* = 0.4237 - 0.00821 \times (6 - A)^2

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: :math:`a_0^*` value.
        :rtype: float
        """
        observer_altitude_km = self._convert_to_km(observer_altitude)
        observer_altitude_diff = 6.0 - observer_altitude_km
        return 0.4237 - 0.00821 * observer_altitude_diff**2

    def _calculate_a1_star(self, observer_altitude: int) -> float:
        r"""
        Calculate :math:`a_1^*` based on observer altitude.

        The formula used to calculate :math:`a_1^*` is:

        .. math::
            a_1^* = 0.5055 + 0.00595 \times (6.5 - A)^2

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: :math:`a_1^*` value.
        :rtype: float
        """
        observer_altitude_km = self._convert_to_km(observer_altitude)
        observer_altitude_diff = 6.5 - observer_altitude_km
        return 0.5055 + 0.00595 * observer_altitude_diff**2

    def _calculate_k_star(self, observer_altitude: int) -> float:
        r"""
        Calculate :math:`k^*` based on observer altitude.

        The formula used to calculate :math:`k^*` is:

        .. math::
            k^* = 0.2711 + 0.01858 \times (2.5 - A)^2

        :param observer_altitude: Altitude of the observer in meters.
        :type observer_altitude: float
        :return: :math:`k^*` value.
        :rtype: float
        """
        observer_altitude_km = self._convert_to_km(observer_altitude)
        observer_altitude_diff = 2.5 - observer_altitude_km
        return 0.2711 + 0.01858 * observer_altitude_diff**2

    def calculate_transmittance_components(
        self, climate_type: str, observer_altitude: int
    ) -> Tuple[float, float, float]:
        r"""
        Calculate the components of clear-sky beam radiation transmittance
        :math:`a_0`, :math:`a_1`, and :math:`k`
        based on climate type and observer altitude.

        Correction factors adjust the clear-sky beam
        radiation transmittance components according to the following formulas:

        .. math::
            a_0 = r_0 \times a_0^*

            a_1 = r_1 \times a_1^*

            k = r_k \times k^*

        The formula used to calculate :math:`a_0^*` is:

        .. math::
            a_0^* = 0.4237 - 0.00821 \times (6 - A)^2

        The formula used to calculate :math:`a_1^*` is:

        .. math::
            a_1^* = 0.5055 + 0.00595 \times (6.5 - A)^2

        The formula used to calculate :math:`k^*` is:

        .. math::
            k^* = 0.2711 + 0.01858 \times (2.5 - A)^2

        Where `A` is the observer altitude in kilometers.

        :param climate_type: Climate type (i.e., one of the keys in
                            `Climate Constants`: ``TROPICAL``, ``MIDLATITUDE SUMMER``,
                            ``SUBARCTIC SUMMER``, or ``MIDLATITUDE WINTER``).
        :type climate_type: str
        :param observer_altitude: Altitude of the observer in meters.
                                It is converted to kilometers in the calculations.
        :type observer_altitude: float
        :return: Components of clear-sky beam radiation transmittance
                (:math:`a_0`, :math:`a_1`, :math:`k`).
        :rtype: tuple of floats
        :raises ValueError: If an invalid climate type is provided.
        """

        self.CLIMATE_CONSTANTS: Dict[str, Tuple[float, float, float]] = {
            "TROPICAL": (0.95, 0.98, 1.02),
            "MIDLATITUDE SUMMER": (0.97, 0.99, 1.02),
            "SUBARCTIC SUMMER": (0.99, 0.99, 1.01),
            "MIDLATITUDE WINTER": (1.03, 1.01, 1.00),
        }

        if climate_type.upper() not in self.CLIMATE_CONSTANTS:
            raise ValueError("Invalid climate type")

        r0, r1, rk = self.CLIMATE_CONSTANTS[climate_type.upper()]

        a0_star = self._calculate_a0_star(observer_altitude)
        a1_star = self._calculate_a1_star(observer_altitude)
        k_star = self._calculate_k_star(observer_altitude)

        return r0 * a0_star, r1 * a1_star, rk * k_star
