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
    def solar_declination(self, day_of_year: int) -> float:
        r"""
        Calculate the solar declination angle in radians.

        The solar declination angle is the angle between the rays of the sun
        and the plane of the Earth's equator.

        The formula used to calculate the solar declination angle is:

        .. math::
            \delta = \sin \left( \frac{2 \pi}{365}
            \times (284 + \text{{day\_of\_year}}) \right)
            \times \left(\frac{23.45 \pi}{180}\right)

        :param day_of_year: The day of the year.
        :type day_of_year: int
        :return: The solar declination angle in radians.
        :rtype: float
        """
        # tilt of the Earth's axis (in degrees)
        earth_tilt_degrees = 23.45

        # Convert the tilt to radians
        earth_tilt_radians = math.radians(earth_tilt_degrees)

        # Offset to ensure declination angle is zero at the March equinox
        equinox_offset_days = 284

        # Calculate the solar declination angle
        solar_declination = (
            math.sin((2 * math.pi) * (equinox_offset_days + day_of_year) / 365)
            * earth_tilt_radians
        )

        return solar_declination

    def hour_angle(self, solar_time: float) -> float:
        r"""
        Calculate the hour angle based on the solar time.

        The hour angle is a measure of time, expressed in angular terms,
        from solar noon.

        The formula used to calculate the hour angle is:

        .. math::
            \omega = (t - \text{{seconds\_in\_half\_day}})
            \times \frac{\pi}{\text{{seconds\_in\_half\_day}}}

        :param solar_time: The solar time in seconds.
        :type solar_time: float
        :return: The hour angle in radians.
        :rtype: float
        """
        # The number of seconds in half a day (12 hours)
        seconds_in_half_day = 12 * 60 * 60

        # The Earth rotates by pi/seconds_in_half_day radians per second
        earth_rotation_rate = math.pi / seconds_in_half_day

        # Calculate the hour angle
        hour_angle = (solar_time - seconds_in_half_day) * earth_rotation_rate

        return hour_angle

    def solar_time(self, hour_angle: float) -> float:
        r"""
        Calculate the solar time based on the hour angle.

        The solar time is a measure of time, expressed in seconds, from solar noon.

        The formula used to calculate the solar time is:

        .. math::
            t = \omega \times \frac{\text{{seconds\_in\_half\_day}}}{\pi}
            + \text{{seconds\_in\_half\_day}}

        :param hour_angle: The hour angle in radians.
        :type hour_angle: float
        :return: The solar time in seconds.
        :rtype: float
        """
        # The number of seconds in half a day (12 hours)
        seconds_in_half_day = 12 * 60 * 60

        # The Earth rotates by pi/seconds_in_half_day radians per second
        earth_rotation_rate = math.pi / seconds_in_half_day

        # Calculate the solar time
        solar_time = hour_angle / earth_rotation_rate + seconds_in_half_day

        return solar_time
