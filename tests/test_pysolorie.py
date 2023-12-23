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
import csv
import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import numpy as np
import pytest

from pysolorie import (
    AtmosphericTransmission,
    IrradiationCalculator,
    Plotter,
    ReportGenerator,
)


@pytest.mark.parametrize(
    "climate_type,"
    + "observer_altitude,"
    + "observer_latitude,"
    + "day_of_year,"
    + "solar_time,"
    + "expected_transmittance",
    [
        ("MIDLATITUDE SUMMER", 1200, 35.69, 81, 12 * 60 * 60, 0.683),  # Tehran Summer
        ("MIDLATITUDE WINTER", 1200, 35.69, 355, 12 * 60 * 60, 0.618),  # Tehran Winter
        ("TROPICAL", 63, 3.59, 81, 10 * 60 * 60, 0.597),  # Medan
        ("SUBARCTIC SUMMER", 136, 64.84, 1, 13 * 60 * 60, 0.140),  # Fairbanks
    ],
)
def test_calculate_transmittance(
    climate_type: str,
    observer_altitude: int,
    observer_latitude: float,
    day_of_year: int,
    solar_time: float,
    expected_transmittance: float,
) -> None:
    atmospheric_transmission: AtmosphericTransmission = AtmosphericTransmission(
        climate_type, observer_altitude, observer_latitude
    )
    result: float = atmospheric_transmission.calculate_transmittance(
        day_of_year, solar_time
    )
    assert pytest.approx(result, abs=1e-3) == expected_transmittance


@pytest.mark.parametrize(
    "climate_type,"
    + "observer_altitude,"
    + "observer_latitude,"
    + "day_of_year,"
    + "panel_orientation,"
    + "expected_result",
    [
        (
            "MIDLATITUDE SUMMER",
            1200,
            35.6892,
            172,
            45.0,
            20.3026,  # Tehran Summer, day_of_year=172 (June 21)
        ),
        (
            "MIDLATITUDE WINTER",
            1200,
            35.6892,
            355,
            45.0,
            19.436,  # Tehran Winter, day_of_year=355 (Dec 21)
        ),
        (
            "TROPICAL",
            26,
            3.5952,
            100,
            45.0,
            13.224,  # Medan, day_of_year=100 (April 10)
        ),
        (
            "SUBARCTIC SUMMER",
            132,
            64.84361,
            200,
            45.0,
            21.371,  # Fairbanks Summer, day_of_year=200 (July 19)
        ),
    ],
)
def test_calculate_direct_irradiation(
    climate_type: str,
    observer_altitude: int,
    observer_latitude: float,
    day_of_year: int,
    panel_orientation: float,
    expected_result: float,
) -> None:
    irradiation_calculator = IrradiationCalculator(
        climate_type, observer_altitude, observer_latitude
    )
    result = irradiation_calculator.calculate_direct_irradiation(
        panel_orientation, day_of_year
    )
    assert pytest.approx(result, abs=1e-3) == expected_result


@pytest.mark.parametrize(
    "climate_type, observer_altitude, observer_latitude, day_of_year, expected_result",
    [
        (
            "MIDLATITUDE SUMMER",
            1200,
            35.6892,
            172,
            0.170,
        ),  # Tehran Summer, day_of_year=172 (June 21)
        (
            "MIDLATITUDE WINTER",
            1200,
            35.6892,
            355,
            63.791,
        ),  # Tehran Winter, day_of_year=355 (Dec 21)
        (
            "TROPICAL",
            26,
            3.5952,
            100,
            -6.610,
        ),  # Medan, day_of_year=100 (April 10)
        (
            "SUBARCTIC SUMMER",
            132,
            64.84361,
            200,
            32.614,
        ),  # Fairbanks Summer, day_of_year=200 (July 19)
    ],
)
def test_find_optimal_orientation(
    climate_type: str,
    observer_altitude: int,
    observer_latitude: float,
    day_of_year: int,
    expected_result: float,
) -> None:
    irradiation_calculator = IrradiationCalculator(
        climate_type, observer_altitude, observer_latitude
    )
    result = irradiation_calculator.find_optimal_orientation(day_of_year)
    assert pytest.approx(result, abs=1e-3) == expected_result


def test_generate_optimal_orientation_csv_report(caplog, tmpdir) -> None:
    caplog.set_level(logging.INFO)

    # Create a temporary directory for the test
    temp_dir: Path = Path(tmpdir)

    # Initialize the ReportGenerator
    report_generator: ReportGenerator = ReportGenerator()

    # Initialize the IrradiationCalculator for Tehran
    irradiation_calculator: IrradiationCalculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Define the path for the CSV file
    csv_path: Path = temp_dir / "report.csv"
    from_day: int = 60
    to_day: int = 70
    # Call the method to generate the report
    report_generator.generate_optimal_orientation_csv_report(
        csv_path, irradiation_calculator, from_day, to_day
    )

    # Check the CSV file
    with open(csv_path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        assert header == [
            "Day",
            "Beta (degrees)",
            "Total Direct Irradiation (Megajoules per square meter)",
        ]
        for i, row in enumerate(reader, start=from_day):
            day, beta, total_direct_irradiation = (
                int(row[0]),
                float(row[1]),
                float(row[2]),
            )

            assert day == i
            expected_beta = irradiation_calculator.find_optimal_orientation(i)

            expected_total_direct_irradiation = (
                irradiation_calculator.calculate_direct_irradiation(beta, i)
            )
            assert pytest.approx(beta, abs=1e-3) == expected_beta
            assert (
                pytest.approx(total_direct_irradiation, abs=1e-3)
                == expected_total_direct_irradiation
            )
    # Check the logs
    for day in range(from_day, to_day):
        assert any(
            f"On day {day}," in record.message for record in caplog.records
        ), f"No log message for day {day}"


def test_generate_optimal_orientation_json_report(caplog, tmpdir) -> None:
    caplog.set_level(logging.INFO)

    # Create a temporary directory for the test
    temp_dir: Path = Path(tmpdir)

    # Initialize the ReportGenerator
    report_generator: ReportGenerator = ReportGenerator()

    # Initialize the IrradiationCalculator for Tehran
    irradiation_calculator: IrradiationCalculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Define the path for the JSON file
    json_path: Path = temp_dir / "report.json"
    from_day: int = 60
    to_day: int = 70
    # Call the method to generate the report
    report_generator.generate_optimal_orientation_json_report(
        json_path, irradiation_calculator, from_day, to_day
    )

    # Check the JSON file
    with open(json_path, "r") as file:
        data = json.load(file)
        for i, row in enumerate(data, start=from_day):
            day, beta, total_direct_irradiation = (
                row["Day"],
                row["Beta (degrees)"],
                row["Total Direct Irradiation (Megajoules per square meter)"],
            )

            assert day == i
            expected_beta = irradiation_calculator.find_optimal_orientation(i)
            expected_total_direct_irradiation = (
                irradiation_calculator.calculate_direct_irradiation(beta, i)
            )
            assert pytest.approx(beta, abs=1e-3) == expected_beta
            assert (
                pytest.approx(total_direct_irradiation, abs=1e-3)
                == expected_total_direct_irradiation
            )
    # Check the logs
    for day in range(from_day, to_day):
        assert any(
            f"On day {day}," in record.message for record in caplog.records
        ), f"No log message for day {day}"


def test_generate_optimal_orientation_xml_report(caplog, tmpdir) -> None:
    caplog.set_level(logging.INFO)

    # Create a temporary directory for the test
    temp_dir: Path = Path(tmpdir)

    # Initialize the ReportGenerator
    report_generator: ReportGenerator = ReportGenerator()

    # Initialize the IrradiationCalculator for Tehran
    irradiation_calculator: IrradiationCalculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Define the path for the XML file
    xml_path: Path = temp_dir / "report.xml"
    from_day: int = 60
    to_day: int = 70
    # Call the method to generate the report
    report_generator.generate_optimal_orientation_xml_report(
        xml_path, irradiation_calculator, from_day, to_day
    )

    # Check the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for i, day_element in enumerate(root.findall("Day"), start=from_day):
        day = int(day_element.get("id"))
        beta = float(day_element.find("Beta").text)
        total_direct_irradiation = float(
            day_element.find("TotalDirectIrradiation").text
        )

        assert day == i
        expected_beta = irradiation_calculator.find_optimal_orientation(i)
        expected_total_direct_irradiation = (
            irradiation_calculator.calculate_direct_irradiation(beta, i)
        )
        assert pytest.approx(beta, abs=1e-3) == expected_beta
        assert (
            pytest.approx(total_direct_irradiation, abs=1e-3)
            == expected_total_direct_irradiation
        )
    # Check the logs
    for day in range(from_day, to_day):
        assert any(
            f"On day {day}," in record.message for record in caplog.records
        ), f"No log message for day {day}"


def test_plot_optimal_orientation(caplog, tmpdir) -> None:
    caplog.set_level(logging.INFO)

    # Create a temporary directory for the test
    temp_dir: Path = Path(tmpdir)

    # Initialize the Plotter
    plotter: Plotter = Plotter()

    # Initialize the IrradiationCalculator for Tehran
    irradiation_calculator: IrradiationCalculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Define the path for the plot
    plot_path: Path = temp_dir / "plot.png"
    from_day: int = 60
    to_day: int = 70
    # Call the method to generate the plot
    plotter.plot_optimal_orientation(
        irradiation_calculator, from_day, to_day, plot_path
    )

    # Check the plot file
    assert plot_path.exists(), "The plot file was not created."

    img: np.ndarray = plt.imread(plot_path)
    assert img.shape[0] > 0, "The plot image has no content."
    assert img.shape[1] > 0, "The plot image has no content."

    # Check the logs
    for day in range(from_day, to_day):
        assert any(
            f"On day {day}," in record.message for record in caplog.records
        ), f"No log message for day {day}"


def test_plot_total_direct_irradiation(caplog, tmpdir) -> None:
    caplog.set_level(logging.INFO)

    # Create a temporary directory for the test
    temp_dir: Path = Path(tmpdir)

    # Initialize the Plotter
    plotter: Plotter = Plotter()

    # Initialize the IrradiationCalculator for Tehran
    irradiation_calculator: IrradiationCalculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Define the path for the plot
    plot_path: Path = temp_dir / "plot.png"
    from_day: int = 60
    to_day: int = 70
    # Call the method to generate the plot
    plotter.plot_total_direct_irradiation(
        irradiation_calculator, from_day, to_day, plot_path
    )

    # Check the plot file
    assert plot_path.exists(), "The plot file was not created."

    img: np.ndarray = plt.imread(plot_path)
    assert img.shape[0] > 0, "The plot image has no content."
    assert img.shape[1] > 0, "The plot image has no content."

    # Check the logs
    for day in range(from_day, to_day):
        assert any(
            f"On day {day}," in record.message for record in caplog.records
        ), f"No log message for day {day}"


def test_plot_method() -> None:
    # Set up the necessary variables
    plotter: Plotter = Plotter()
    days: List[int] = [1, 2, 3]
    betas: List[float] = [10.0, 20.0, 30.0]
    path: None = None
    plot_kwargs: Dict[str, Any] = {}
    savefig_kwargs: Dict[str, Any] = {}

    # Replace plt.show with a mock
    plt.show = MagicMock()

    # Call the method
    plotter._plot(days, betas, path, plot_kwargs, savefig_kwargs)
    plt.show.assert_called_once()
