#!/usr/bin/env python
# -*- coding: utf-8 -*-


import setuptools
import setuptools.command.test

import surveyor


with open("README.rst", "r") as resource:
    LONG_DESCRIPTION = resource.read()


# copypasted from http://pytest.org/latest/goodpractises.html
# noinspection PyAttributeOutsideInit
class PyTest(setuptools.command.test.test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        setuptools.command.test.initialize_options(self)
        self.pytest_args = None  # pylint: disable=W0201 noqa

    def finalize_options(self):
        setuptools.command.test.finalize_options(self)
        self.test_args = []  # pylint: disable=W0201 noqa
        self.test_suite = True  # pylint: disable=W0201 noqa

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded

        import pytest
        import sys

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setuptools.setup(
    name="surveyor",
    description="Painless XLSX templating",
    long_description=LONG_DESCRIPTION,
    version=".".join(map(str, surveyor.__version__)),
    author="Sergey Arkhipov",
    license="MIT",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    maintainer_email="serge@aerialsounds.org",
    url="https://github.com/9seconds/surveyor/",
    install_requires=[
        "openpyxl>=2.2,<2.3",
        "six"
    ],
    extras_require={
        'fast':  ["lxml"],
    },
    keywords="excel template spreadsheet",
    tests_require=[
        "pytest>=2.6.1"
    ],
    packages=setuptools.find_packages(),
    cmdclass={'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "Topic :: Office/Business :: Financial :: Spreadsheet",

    ],
    zip_safe=False
)
