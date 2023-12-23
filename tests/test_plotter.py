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

import logging
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import numpy as np

from pysolorie import IrradiationCalculator, Plotter


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
