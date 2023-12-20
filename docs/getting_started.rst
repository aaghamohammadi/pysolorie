Getting Started
===============
This guide will help you get started with using the pysolorie library.

How to Install pysolorie
------------------------

``pysolorie`` requires Python 3.9 or higher.

The easiest way to install ``pysolorie``  is from PyPI.

.. code-block:: bash

    $ python3 -m pip install pysolorie



Finding the Optimal Orientation
-------------------------------
The ``find_optimal_orientation`` method finds the optimal orientation for a solar
panel given the climate type, observer altitude, observer latitude, and day of the year.

The ``climate_type`` can be one of the following:

- ``"MIDLATITUDE SUMMER"``
- ``"MIDLATITUDE WINTER"``
- ``"TROPICAL"``
- ``"SUBARCTIC SUMMER"``


.. code-block:: python

    from pysolorie import IrradiationCalculator

    # Create an irradiation calculator for Tehran in the summer
    irradiation_calculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Find the optimal orientation for June 21st
    result = irradiation_calculator.find_optimal_orientation(172)

    print(f"Optimal orientation: {result}")

Calculating Direct Irradiation
------------------------------
The ``calculate_direct_irradiation`` method calculates the total direct irradiation for a given solar panel orientation and day of the year.

The ``climate_type`` can be one of the following:

- ``"MIDLATITUDE SUMMER"``
- ``"MIDLATITUDE WINTER"``
- ``"TROPICAL"``
- ``"SUBARCTIC SUMMER"``

.. code-block:: python

    from pysolorie import IrradiationCalculator

    # Create an irradiation calculator for Tehran in the summer
    irradiation_calculator = IrradiationCalculator(
        "MIDLATITUDE SUMMER", 1200, 35.6892
    )

    # Define the panel orientation and day of the year
    panel_orientation: float = 45.0  # degrees
    day_of_year: int = 172  # June 21, approximately the summer solstice

    # Calculate the direct irradiation
    result = irradiation_calculator.calculate_direct_irradiation(panel_orientation, day_of_year)

    print(f"Direct irradiation: {result}")


Generating a CSV Report
-----------------------

The ``generate_optimal_orientation_csv_report`` method generates a CSV report of
the optimal orientation for a range of days.

.. code-block:: python

    from pysolorie import ReportGenerator, IrradiationCalculator
    from pathlib import Path

    # Create a report generator and an irradiation calculator
    report_generator = ReportGenerator()
    irradiation_calculator = IrradiationCalculator("MIDLATITUDE SUMMER", 1200, 35.6892)

    # Generate a CSV report for days 60 to 70
    report_generator.generate_optimal_orientation_csv_report(Path('results.csv'), irradiation_calculator, 60, 70)

The CSV file will be saved to the specified path.


Plotting the Optimal Orientation
--------------------------------

The ``plot_optimal_orientation`` method plots the optimal orientation for a range of days.

.. code-block:: python

    from pysolorie import Plotter, IrradiationCalculator
    from pathlib import Path

    # Create a plotter and an irradiation calculator
    plotter = Plotter()
    irradiation_calculator = IrradiationCalculator("MIDLATITUDE SUMMER", 1200, 35.6892)

    # Plot the optimal orientation for days 60 to 70
    plotter.plot_optimal_orientation(irradiation_calculator, 60, 70, Path('results.png'), plot_kwargs={'xlabel': 'Day', 'ylabel': 'Beta (degrees)', 'title': 'Optimal Solar Panel Orientation', "figsize": (16,9)}, savefig_kwargs={'dpi': 300})

The plot will be saved to the specified path. The ``plot_kwargs`` and ``savefig_kwargs``
parameters can be used to customize the plot and the savefig function, respectively. If no path is provided, the plot will be displayed but not saved.
If the path is provided, the plot will be saved to the specified path and not displayed. If you want to both display and save the plot, you should call ``plt.show()`` after this function.

Plotting the Total Direct Irradiation
-------------------------------------

The ``plot_total_direct_irradiation`` method plots the total direct irradiation for a range of days.

.. code-block:: python

    from pysolorie import Plotter, IrradiationCalculator
    from pathlib import Path

    # Create a plotter and an irradiation calculator
    plotter = Plotter()
    irradiation_calculator = IrradiationCalculator("MIDLATITUDE SUMMER", 1200, 35.6892)

    # Plot the total direct irradiation for days 60 to 70
    plotter.plot_total_direct_irradiation(irradiation_calculator, 60, 70, Path('results.png'), plot_kwargs={'xlabel': 'Day', 'ylabel': 'Total Direct Irradiation (MW/m²)', 'title': 'Total Direct Irradiation', "figsize": (16,9)}, savefig_kwargs={'dpi': 300})

The plot will be saved to the specified path. The ``plot_kwargs`` and ``savefig_kwargs``
parameters can be used to customize the plot and the savefig function, respectively. If no path is provided, the plot will be displayed but not saved.
If the path is provided, the plot will be saved to the specified path and not displayed. If you want to both display and save the plot, you should call ``plt.show()`` after this function.




Calculating Sunrise and Sunset
------------------------------

The ``calculate_sunrise_sunset`` method calculates the sunrise and sunset hour angles
for a given day of the year.

.. code-block:: python

    from pysolorie import Observer

    # Create an observer located in Tehran
    observer = Observer(observer_latitude=35.69)

    # Calculate the sunrise and sunset hour angles for June 21st
    sunrise_hour_angle, sunset_hour_angle = observer.calculate_sunrise_sunset(172)

    print(f"Sunrise hour angle: {sunrise_hour_angle}")
    print(f"Sunset hour angle: {sunset_hour_angle}")


Calculating the Solar Zenith Angle
----------------------------

The ``calculate_zenith_angle`` method calculates the zenith angle given the day of the year
and solar time.


.. code-block:: python

    from pysolorie import Observer

    # Create an observer located in Tehran (latitude 35.69, longitude 51.39)
    observer = Observer(35.69, 51.39)

    # Calculate the zenith angle for March 22nd (81st day of the year) at solar noon (12 * 60 * 60 seconds)
    zenith_angle = observer.calculate_zenith_angle(81, 12 * 60 * 60)

    print(f"Zenith angle: {zenith_angle}")

Note that the observer's latitude must be provided when creating an ``Observer`` instance.
If it's not provided, a ``ValueError`` will be raised:

.. code-block:: python

    from pysolorie import Observer

    # Attempt to create an observer without specifying the latitude
    try:
        observer = Observer(None, 0)
        observer.calculate_zenith_angle(1, 12 * 60 * 60)
    except ValueError as e:
        print(f"Caught an exception: {e}")

Calculating Solar Time
----------------------

The ``solar_time`` method calculates the solar time given the hour angle.


.. code-block:: python

    from pysolorie import SunPosition

    # Create a SunPosition instance
    sun_position = SunPosition()

    # Calculate the solar time for solar noon (hour angle 0)
    solar_time = sun_position.solar_time(0)

    print(f"Solar time: {solar_time}")

This will print the solar time in seconds. For example,
solar noon (when the sun is at its highest point in the sky)
corresponds to ``12 * 60 * 60 = 43200`` seconds.

Calculating Solar Declination and Hour Angle
--------------------------------------------

The ``solar_declination`` method calculates the solar declination given the day of the year,
and the ``hour_angle`` method calculates the hour angle given the solar time.

.. code-block:: python

    from pysolorie import SunPosition

    # Create a SunPosition instance
    sun_position = SunPosition()

    # Calculate the solar declination for January 1st
    declination = sun_position.solar_declination(1)

    # Calculate the hour angle for 1pm (13 * 60 * 60 seconds)
    hour_angle = sun_position.hour_angle(13 * 60 * 60)

    print(f"Solar declination: {declination}")
    print(f"Hour angle: {hour_angle}")

This will print the solar declination and hour angle in radians.
For example, on January 1st at 1pm, the solar declination is approximately ``-0.401`` radians and the hour angle is approximately ``0.262`` radians.

Calculating Transmittance Components with the Hottel Model
----------------------------------------------------------

The Hottel Model is used for estimating clear-sky beam radiation transmittance based on climate type and observer altitude. The `calculate_transmittance_components` method of the `HottelModel` class calculates the components of clear-sky beam radiation transmittance :math:`a_0`, :math:`a_1`, and :math:`k` based on climate type and observer altitude.

.. code-block:: python

    from pysolorie import HottelModel

    # Create a HottelModel instance
    hottel_model = HottelModel()

    # Calculate the transmittance components for Tehran in the summer at an altitude of 1200m
    result = hottel_model.calculate_transmittance_components("MIDLATITUDE SUMMER", 1200)

    print(f"Transmittance components: {result}")

This will print the transmittance components as a tuple of three values. For example, for Tehran in the summer at an altitude of 1200m, the transmittance components are approximately ``(0.228, 0.666, 0.309)``.

The ``climate_type`` parameter can be one of the following:

- ``"TROPICAL"``
- ``"MIDLATITUDE SUMMER"``
- ``"SUBARCTIC SUMMER"``
- ``"MIDLATITUDE WINTER"``

If an invalid climate type is provided, a ``ValueError`` will be raised.
