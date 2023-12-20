# Copyright 2023 Alireza Aghamohammadi

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt  # type: ignore

from .logger import logger_decorator
from .numerical_integration import IrradiationCalculator


class Plotter:
    r"""
    A class used to plot the optimal orientation of a solar panel.
    """

    @logger_decorator
    def plot_optimal_orientation(
        self,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
        path: Optional[Path] = None,
        plot_kwargs: Optional[Dict[str, str]] = None,
        savefig_kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        r"""
        Plots the optimal orientation of a solar panel for a range of days.

        :param irradiation_calculator: An instance of the IrradiationCalculator class.
        :type irradiation_calculator: pysolorie.IrradiationCalculator
        :param from_day: The starting day for the range of days.
        :type from_day: int
        :param to_day: The ending day for the range of days.
        :type to_day: int
        :param path: The path where the plot will be saved (default is None,
                     which means the plot will be shown but not saved).
        :type path: Path, optional
        :param plot_kwargs: A dictionary of keyword arguments
                            to be passed to the plot (default is None).
        :type plot_kwargs: dict, optional
        :param savefig_kwargs: A dictionary of keyword arguments
                               to be passed to the savefig function (default is None).
        :type savefig_kwargs: dict, optional
        """

        days, betas = self._calculate_optimal_orientations(
            irradiation_calculator, from_day, to_day
        )

        plot_kwargs = plot_kwargs if plot_kwargs else {}
        savefig_kwargs = savefig_kwargs if savefig_kwargs else {}

        self._plot(days, betas, path, plot_kwargs, savefig_kwargs)

    @logger_decorator
    def plot_total_direct_irradiation(
        self,
        irradiation_calculator: IrradiationCalculator,
        from_day: int,
        to_day: int,
        path: Optional[Path] = None,
        plot_kwargs: Optional[Dict[str, str]] = None,
        savefig_kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        r"""
        Plots the total direct irradiation for a range of days.

        :param irradiation_calculator: An instance of the IrradiationCalculator class.
        :type irradiation_calculator: pysolorie.IrradiationCalculator
        :param from_day: The starting day for the range of days.
        :type from_day: int
        :param to_day: The ending day for the range of days.
        :type to_day: int
        :param path: The path where the plot will be saved (default is None,
                    which means the plot will be shown but not saved).
        :type path: Path, optional
        :param plot_kwargs: A dictionary of keyword arguments
                            to be passed to the plot (default is None).
        :type plot_kwargs: dict, optional
        :param savefig_kwargs: A dictionary of keyword arguments
                            to be passed to the savefig function (default is None).
        :type savefig_kwargs: dict, optional
        """

        days = []
        total_direct_irradiations = []

        for day in range(from_day, to_day):
            optimal_beta = irradiation_calculator.find_optimal_orientation(day)
            total_direct_irradiation = (
                irradiation_calculator.calculate_direct_irradiation(optimal_beta, day)
            )
            days.append(day)
            total_direct_irradiations.append(total_direct_irradiation)

        plot_kwargs = plot_kwargs if plot_kwargs else {}
        savefig_kwargs = savefig_kwargs if savefig_kwargs else {}

        self._plot(days, total_direct_irradiations, path, plot_kwargs, savefig_kwargs)

    def _calculate_optimal_orientations(
        self, irradiation_calculator: IrradiationCalculator, from_day: int, to_day: int
    ) -> Tuple[List[int], List[float]]:
        days = []
        betas = []

        for day in range(from_day, to_day):
            beta = irradiation_calculator.find_optimal_orientation(day)
            logger = logging.getLogger(self.plot_optimal_orientation.__name__)
            logger.info(
                f"On day {day},"
                + f"the solar panel's optimal orientation is {beta} degrees."
            )
            days.append(day)
            betas.append(beta)

        return days, betas

    def _plot(
        self,
        days: List[int],
        betas: List[float],
        path: Optional[Path],
        plot_kwargs: Dict[str, str],
        savefig_kwargs: Dict[str, str],
    ) -> None:
        figsize = plot_kwargs.get("figsize", (10, 6))
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(days, betas)
        ax.set_xlabel(plot_kwargs.get("xlabel", "X Axis Title"))
        ax.set_ylabel(plot_kwargs.get("ylabel", "Y Axis Title"))
        ax.set_title(plot_kwargs.get("title", "Title"))
        ax.grid(True)

        if path is not None:
            plt.savefig(path, **savefig_kwargs)
        else:
            plt.show()
