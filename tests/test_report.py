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

import pytest

from pysolorie import IrradiationCalculator, ReportGenerator


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
