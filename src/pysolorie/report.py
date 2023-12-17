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
import logging
from pathlib import Path

from .logger import logger_decorator
from .numerical_integration import IrradiationCalculator


class ReportGenerator:
    @logger_decorator
    def generate_optimal_orientation_csv_report(
        self,
        path: Path,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
    ) -> None:
        r"""
        This method generates a report of
        optimal solar panel orientation in CSV format.

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
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Day", "Beta (degrees)", "Total Direct Irradiation (MW/m²)"]
            )

            for day in range(from_day, to_day):
                beta = irradiation_calculator.find_optimal_orientation(day)
                total_direct_irradiation = (
                    irradiation_calculator.calculate_direct_irradiation(beta, day)
                )
                logger = logging.getLogger(
                    self.generate_optimal_orientation_csv_report.__name__
                )
                logger.info(
                    f"On day {day}, the solar panel's optimal orientation is "
                    f"{beta} degrees, and the total direct irradiation is "
                    f"{total_direct_irradiation} MW/m²."
                )

                # Write the result to the CSV file
                writer.writerow([day, beta, total_direct_irradiation])
