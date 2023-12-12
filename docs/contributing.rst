Contributing
============

We welcome contributions to the pysolorie project!
This document will guide you through the process of setting up your development environment,
running tests, and submitting your contributions.

Setting Up Your Development Environment
---------------------------------------

1. **Fork the repository**:

Start by forking the pysolorie repository on GitHub.

2. **Clone the repository**:

Clone your fork of the repository to your local machine using the command ``git clone https://github.com/<your-username>/pysolorie``.

3. **Install Python**:

pysolorie requires Python 3.9 or higher. You can download Python from the official website.

4. **Setup environment**:

It is highly recommended to use ``virtualenv`` for the development. ``virtualenv`` is a tool to create isolated Python environments.

    .. code-block:: bash

        $ python3 -m venv .venv
        $ source .venv/bin/activate
        $ pip install -r dev-requirements.txt

5. **Install pre-commit**:

We use ``pre-commit`` hooks for some validation before letting you push to the
remote repository. ``pre-commit`` is a tool that manages and maintains multi-language pre-commit hooks.

    .. code-block:: bash

        $ pre-commit install


Running Tests
-------------

We use ``tox`` to run our tests. ``tox`` is a generic virtualenv management and test command-line tool.
The ``setup.cfg`` file in the root of the repository defines several test environments:

- ``format``: Checks the formatting of the code with black.
- ``lint``: Runs the flake8 linter on the code.
- ``typecheck``: Checks the types in the code with mypy.
- ``py311``, ``py310``, ``py39``: Runs the test suite with pytest on Python 3.11, 3.10, and 3.9 respectively.

You can run these tests locally with the ``tox -e`` command.
For example, to run the linter, you would use the following command:

    .. code-block:: bash

        $ tox -e lint

If you want to reformat the source code. You can use the following command:

    .. code-block:: bash

        $ tox -e format -- src tests

To verify the correctness of the formatting, execute the command below:

    .. code-block:: bash

        $ tox -e format

To check the types in the code with mypy, use this:

    .. code-block:: bash

        $ tox -e typecheck

To run unit tests for the python, e.g., python 3.10, you can run this command:

    .. code-block:: bash

        $ tox -e py310

Submitting Your Contributions
-----------------------------

Contributions to the pysolorie project can start with writing test cases. This is a great way to understand the project and ensure its robustness. Once you've made your changes and all tests are passing, you can submit your contributions by creating a pull request on GitHub.

**We are also looking to add plotting support to the project.** If you're interested, you could start by looking into libraries like matplotlib or other similar tools. However, it's important to note that we aim to keep our dependencies minimal. Any new dependency should be clearly justified and absolutely necessary.

When submitting your contributions, please make sure to include a clear and detailed description of your changes. Before submitting new ones, please check the existing issues and pull requests to avoid duplication.

Thank you for contributing to pysolorie!
