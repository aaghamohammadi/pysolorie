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
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Union

from .logger import logger_decorator
from .numerical_integration import IrradiationCalculator


class ReportGenerator:
    r"""
    A class to generate reports for the optimal orientation
    of solar panels and the total direct irradiation.
    """

    @logger_decorator
    def _calculate_optimal_orientation_and_irradiation(
        self,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
    ) -> List[Dict[str, Union[int, float]]]:
        r"""
        This private method calculates the optimal solar panel orientation and
        total direct irradiation for a range of days.

        :param irradiation_calculator: An instance of the IrradiationCalculator class.
        :type irradiation_calculator: pysolorie.IrradiationCalculator
        :param from_day: The starting day of the report.
        :type from_day: int
        :param to_day: The ending day of the report.
        :type to_day: int
        :return: A list of dictionaries, each containing the day,
                 optimal orientation (beta),
                 and total direct irradiation.
        :rtype: List[Dict[str, Union[int, float]]]
        """
        data = []

        for day in range(from_day, to_day):
            beta = irradiation_calculator.find_optimal_orientation(day)
            total_direct_irradiation = (
                irradiation_calculator.calculate_direct_irradiation(beta, day)
            )

            self.logger.info(  # type: ignore
                f"On day {day}, the solar panel's optimal orientation is "
                f"{beta} degrees, and the total direct irradiation is "
                f"{total_direct_irradiation} Megajoules per square meter."
            )

            # Append the result to the data list
            data.append(
                {
                    "Day": day,
                    "Beta (degrees)": beta,
                    "Total Direct Irradiation "
                    "(Megajoules per square meter)": total_direct_irradiation,
                }
            )

        return data

    @logger_decorator
    def generate_optimal_orientation_csv_report(
        self,
        path: Path,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
    ) -> None:
        r"""
        This method generates a report of optimal solar panel orientation in CSV format.
        It uses the ``_calculate_optimal_orientation_and_irradiation``
        method to get the data.

        :param path: A Path object that points to the CSV file
                    where the report will be written.
        :type path: Path
        :param irradiation_calculator: An instance of the IrradiationCalculator class.
        :type irradiation_calculator: pysolorie.IrradiationCalculator
        :param from_day: The starting day of the report.
        :type from_day: int
        :param to_day: The ending day of the report.
        :type to_day: int
        """
        data = self._calculate_optimal_orientation_and_irradiation(
            irradiation_calculator, from_day, to_day
        )

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Day",
                    "Beta (degrees)",
                    "Total Direct Irradiation (Megajoules per square meter)",
                ]
            )

            for row in data:
                writer.writerow(
                    [
                        row["Day"],
                        row["Beta (degrees)"],
                        row["Total Direct Irradiation (Megajoules per square meter)"],
                    ]
                )

    @logger_decorator
    def generate_optimal_orientation_json_report(
        self,
        path: Path,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
    ) -> None:
        r"""
        This method generates a report of optimal
        solar panel orientation in JSON format.
        It uses the ``_calculate_optimal_orientation_and_irradiation``
        method to get the data.

        :param path: A Path object that points to the JSON file
                    where the report will be written.
        :type path: Path
        :param irradiation_calculator: An instance of the IrradiationCalculator class.
        :type irradiation_calculator: pysolorie.IrradiationCalculator
        :param from_day: The starting day of the report.
        :type from_day: int
        :param to_day: The ending day of the report.
        :type to_day: int
        """
        data = self._calculate_optimal_orientation_and_irradiation(
            irradiation_calculator, from_day, to_day
        )

        # Write the data list to the JSON file
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    @logger_decorator
    def generate_optimal_orientation_xml_report(
        self,
        path: Path,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
    ) -> None:
        r"""
        This method generates a report of optimal solar panel orientation in XML format.
        It uses the ``_calculate_optimal_orientation_and_irradiation``
        method to get the data.

        :param path: A Path object that points to the XML file
                    where the report will be written.
        :type path: Path
        :param irradiation_calculator: An instance of the IrradiationCalculator class.
        :type irradiation_calculator: pysolorie.IrradiationCalculator
        :param from_day: The starting day of the report.
        :type from_day: int
        :param to_day: The ending day of the report.
        :type to_day: int
        """
        data = self._calculate_optimal_orientation_and_irradiation(
            irradiation_calculator, from_day, to_day
        )

        # Create the root element
        root = ET.Element("Report")

        for row in data:
            # Create a 'Day' element for each day
            day_element = ET.SubElement(root, "Day")
            day_element.set("id", str(row["Day"]))

            # Create 'Beta' and 'TotalDirectIrradiation' elements for each day
            beta_element = ET.SubElement(day_element, "Beta")
            beta_element.text = str(row["Beta (degrees)"])
            tdi_element = ET.SubElement(day_element, "TotalDirectIrradiation")
            tdi_element.text = str(
                row["Total Direct Irradiation (Megajoules per square meter)"]
            )

        # Write the XML data to the file
        tree = ET.ElementTree(root)
        tree.write(path)
