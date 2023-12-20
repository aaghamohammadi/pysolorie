Changelog
=========

Version 1.5.0
-------------

Release date: 2023-12-20

Added
^^^^^
- Added badges for CodeQL, pre-commit, and code style (black) in README.md, enhancing the visibility of code quality and style adherence.
- Implemented ``generate_optimal_orientation_json_report`` method for JSON report generation in ``ReportGenerator``.
- Developed ``generate_optimal_orientation_xml_report`` method in ``ReportGenerator`` for producing XML formatted reports.
- Expanded ``test_pysolorie.py`` with tests for JSON (``test_generate_optimal_orientation_json_report``) and XML (``test_generate_optimal_orientation_xml_report``) report generation.

Changed
^^^^^^^
- Updated ``plot_total_direct_irradiation`` method's ``ylabel`` argument to use "Megajoules per square meter" instead of "MW/m²" for clarity and accuracy in ``plotter.py``.
- Refactored ``plot_total_direct_irradiation`` in ``Plotter`` to use a private method for calculating optimal orientations, streamlining the plotting process.

Fixed
^^^^^
- Altered the ``Plotter`` methods to handle axis labels and titles through dynamic ``plot_kwargs``, making the labeling more robust and customizable.
- Harmonized and corrected unit values and labelings across the entire codebase and documentation for consistency and accuracy.
- Refined the ``ReportGenerator`` generate methods' docstrings, clearly specifying the return value unit as "Megajoules per square meter".
- Changed the calculation of the solar irradiance formula in ``SolarIrradiance`` from ``0.33`` to ``0.033`` to correct the eccentricity correction factor according to established astronomical equations.


Documentation
^^^^^^^^^^^^^
- Enhanced documentation in ``getting_started.rst`` with examples and instructions for the new JSON and XML report generation methods.
- Altered the representation of solar irradiance units in documentation to match the codebase changes.

Testing
^^^^^^^
- Enriched ``test_pysolorie.py`` with further assertions for newly added JSON and XML report functionalities, ensuring correct report file creation and data integrity.



Version 1.4.0
-------------

Release date: 2023-12-18

Added
^^^^^
- Added ``plot_total_direct_irradiation`` method in the Plotter class for plotting total direct irradiation over a specified range of days with an example included in getting_started.rst.

Changed
^^^^^^^
- Streamlined ``setup.cfg`` to remove unnecessary sphinx-apidoc commands.
- Optimized numerical integration methods to use radians and improved precision settings.
- Updated CSV report generation in ``ReportGenerator`` to include total direct irradiation in output.

Documentation
^^^^^^^^^^^^^
- Implemented significant restructuring and simplifying of the reStructuredText (rst) documentation across many files (modules.rst and individual module documentation).
- Updated module titles to match functionality more accurately, such as "Atmospheric Transmission" and "Hottel Model" for improved clarity in the table of contents.
- Standardized and enhanced docstrings in all module scripts to include detailed descriptions and references where applicable.


Testing
^^^^^^^
- Extended tests in ``test_pysolorie.py`` for additional coverage of new features.

Bug Fixes
^^^^^^^^^
- Corrected the value and unit of the solar constant in ``SolarIrradiance`` from Watts to Megawatts per square meter.


Version 1.3.1
-------------

Release date: 2023-12-16

Added
^^^^^
- An image has been added to the README file, with the solar panel's picture and width specified as 600. (``docs/_static/images/solar_panel.svg``)

Changed
^^^^^^^
- Correction of typographical error in the README.md, changing “Solar Orie” to “Sol Orie” in the abbreviation of “pysolorie”.
- Updated the utilization description from “the Hottel Model” to “Hottel's Model” in the README.md.

Documentation
^^^^^^^^^^^^^
- A detailed explanation of the factors affecting solar irradiation energy received by a solar panel. It includes time of irradiation, latitude and climate of the location, and the solar panel's shape and orientation.
- Mention of how solar collectors can be positioned and adjusted for fixed periods or optimal annual performance.
- Description of the components of solar irradiation: direct beam, sky diffusion, and ground reflection.
- Clarification that the library is now considering flat solar panels and focusing on direct beam irradiation.
- Usage of Hottel's model to estimate the transmittance of direct solar radiation through clear atmospheres.
- A new “References” section with three references to support the text added to the Introduction.
- In the introduction, the leading question has been rephrased for clarity.
- Updated the feature listing of “Calculating the zenith angle” to “Calculating the solar zenith angle”.

Testing
^^^^^^^
- New test case: ``test_generate_optimal_orientation_csv_report`` has been added to verify the functionality of generating CSV reports for the optimal orientation of solar panels over a specified range of days. This test ensures that the CSV file is created correctly and contains the expected data.
- New test case: ``test_plot_optimal_orientation`` is introduced to test the generation of plots for the optimal orientation. It checks if the plot file is created and has content, ensuring that the visual representation of the data is correctly generated.
- New test case: ``test_plot_method`` to verify internal plotting functionality. This test covers the private method ``_plot``, which underlies the plotting functionality. It checks whether the matplotlib library's ``show`` method is called when plotting data without a specified path (used for displaying plots directly).
- The existing test cases have been supplemented with type annotations, providing clearer code documentation and potentially preventing type-related errors. Types such as ``Path``, ``ReportGenerator``, ``IrradiationCalculator``, ``List``, ``Dict``, ``Any``, and several others are now explicitly declared, making the codebase more robust and static type checker friendly.


Version 1.3.0
-------------

Release date: 2023-12-15

Added
^^^^^

- Codecov integration in the GitHub Actions pipeline for Python 3.10.
- Documentation badges including Documentation Status, PyPI Version, PyPI Format, PyPI Status, and Codecov coverage report.
- A new logger module with a logger_decorator for logging the start and finish of functions.
- ReportGenerator and Plotter classes for generating CSV reports and plotting optimal orientations of solar panels.
- Detailed feature listing in the README.md: Providing the added functionalities of generating CSV reports and plotting optimal orientations for a range of days.
- Automated module documentation generation for pysolorie.logger, pysolorie.plotter, and pysolorie.report.
- matplotlib now a dependency, reflecting new plotting capabilities.

Changed
^^^^^^^

- Updated README.md to reflect new library capabilities and contribution guidance.
- Updated contributing section in the documentation, providing clarity on how to contribute and the kinds of contributions welcomed.
- Upgraded Development Status classifier indicating the project is now considered production/stable.

Documentation
^^^^^^^^^^^^^

- Expansive enrichment of the README.md and documentation (``docs/*``), highlighting new features in detail and offering guidance on library usage.
- Detailed description of plotting and generating CSV report functionalities in the getting_started.rst.
- Inclusion of plotting and CSV report generation examples in the documentation.
- Contribution documentation updated to reflect recent changes and guidelines for adding new features and writing test cases.

Testing
^^^^^^^

- Added unit tests for the ReportGenerator and Plotter functionalities.
- pytest is now configured to produce both terminal and XML coverage reports.
