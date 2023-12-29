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

from typing import Optional


class InvalidClimateTypeError(ValueError):
    r"""
    Exception raised for invalid climate type.

    :param climate_type: input climate type which caused the error
    :type climate_type: str
    :param message: explanation of the error, defaults to "Invalid climate type"
    :type message: str, optional
    """

    def __init__(self, climate_type: str, message: Optional[str] = None):
        self.VALID_CLIMATE_TYPES = [
            "TROPICAL",
            "MIDLATITUDE SUMMER",
            "SUBARCTIC SUMMER",
            "MIDLATITUDE WINTER",
        ]
        self.climate_type = climate_type
        if message is None:
            message = (
                f"Invalid climate type: {climate_type}. "
                f"Valid climate types are {', '.join(self.VALID_CLIMATE_TYPES)}"
            )
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        r"""
        String representation of the exception.

        :return: formatted string indicating the invalid
                 climate type and the error message
        :rtype: str
        """
        return f"{self.message}"


class MissingObserverLatitudeError(ValueError):
    r"""
    Exception raised when the observer's latitude is not provided.

    :param message: explanation of the error, defaults to "Missing required data:
                    Observer latitude. Please ensure to provide the latitude of
                    the observer."
    :type message: str, optional
    """

    def __init__(
        self,
        message: str = (
            "Missing required data: Observer latitude. "
            "Please ensure to provide the latitude of the observer."
        ),
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        r"""
        String representation of the exception.

        :return: formatted string indicating the invalid
                 climate type and the error message
        :rtype: str
        """
        return f"{self.message}"


class InvalidObserverLatitudeError(ValueError):
    """
    Exception raised when the observer's latitude is not within the valid range.

    :param message: explanation of the error, defaults to
                    "Invalid data: Observer latitude.
                    Please ensure to provide a latitude between -88 and 88 degrees."
    :type message: str, optional
    """

    def __init__(
        self,
        message: str = (
            "Invalid data: Observer latitude. "
            "Please ensure to provide a latitude between -88 and 88 degrees."
        ),
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        String representation of the exception.

        :return: formatted string indicating the invalid
                 latitude and the error message
        :rtype: str
        """
        return f"{self.message}"
