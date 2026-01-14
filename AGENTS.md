AGENTS.md
=========

This file provides guidance to LLM-based coding agents (such as Claude Code,
OpenCode, Cursor, Windsurf, etc.) when working with code in this repository.


Build & Test Commands
---------------------

~~~~ bash
# Run tests
python -m iso4217.test

# Run linter
flake8 .

# Build distribution
python setup.py sdist bdist_wheel

# Run tests across multiple Python versions
tox
~~~~


Architecture
------------

This is a minimal Python package that provides ISO 4217 currency data as a
Python enum.

**Data flow:**

1.  `setup.py` downloads currency XML data from Six Group (ISO 4217 maintainer)
    to `iso4217/table.xml`
2.  `iso4217/__init__.py` parses the XML at import time and dynamically creates
    enum members

**Key components:**

 -  `Currency` enum with dynamically generated members from XML data (both
    uppercase `Currency.USD` and lowercase `Currency.usd` aliases)
 -  Properties on enum: `code`, `number`, `currency_name`, `country_names`,
    `exponent`

**Version scheme:** `{major}.{minor}.{YYYYMMDD}` where the date comes from the
XML's `Pblshd` attribute

**Environment variables:**

 -  `ISO4217_DOWNLOAD=1` forces re-download of currency data
 -  `ISO4217_DOWNLOAD_URL` overrides the default Six Group URL
