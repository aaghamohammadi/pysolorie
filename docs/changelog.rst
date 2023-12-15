Changelog
=========

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
