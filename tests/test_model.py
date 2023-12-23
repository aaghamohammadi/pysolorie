from typing import Tuple

import pytest

from pysolorie import HottelModel, exceptions


@pytest.mark.parametrize(
    "climate_type, observer_altitude, expected_result",
    [
        ("MIDLATITUDE SUMMER", 1200, (0.228, 0.666, 0.309)),  # Tehran Summer
        ("MIDLATITUDE WINTER", 1200, (0.242, 0.679, 0.303)),  # Tehran Winter
        ("TROPICAL", 26, (0.124, 0.739, 0.392)),  # Medan
        ("SUBARCTIC SUMMER", 136, (0.140, 0.739, 0.379)),  # Fairbanks
    ],
)
def test_calculate_transmittance_components(
    climate_type: str,
    observer_altitude: int,
    expected_result: Tuple[float, float, float],
) -> None:
    hottel_model: HottelModel = HottelModel()
    result: Tuple[
        float, float, float
    ] = hottel_model.calculate_transmittance_components(climate_type, observer_altitude)
    assert pytest.approx(result, abs=1e-3) == expected_result


def test_invalid_climate_type() -> None:
    with pytest.raises(ValueError, match="Invalid climate type"):
        hottel_model: HottelModel = HottelModel()
        hottel_model.calculate_transmittance_components("INVALID", 1000)


def test_invalid_climate_type_with_custom_message() -> None:
    custom_message = "Custom error message"
    with pytest.raises(exceptions.InvalidClimateTypeError, match=custom_message):
        raise exceptions.InvalidClimateTypeError("INVALID", custom_message)
