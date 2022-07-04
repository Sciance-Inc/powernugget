#! /usr/bin/python3

# test_smoketest.py
#
# Project name: Power Nugget
# Author: Hugo Juhel
#
# description:
"""
    Package smoke test. Very high level tests
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

import pytest
from pathlib import Path

#############################################################################
#                                   Script                                  #
#############################################################################


@pytest.fixture
def ngtz():
    """
    Create a Nuggetizer instance
    """

    from powernugget import Nuggetizer

    p = str(Path("tests/test_repo/").absolute())

    return Nuggetizer(path=p)


def test_import():
    """
    Check if the library can be imported
    """

    from powernugget import Nuggetizer


def test_nuggetizer_instanciation():
    """
    Make sure the Nuggetizer can be instanciated
    """

    from powernugget import Nuggetizer

    p = Path("tests/test_repo/").absolute()
    ngtz = Nuggetizer(path=p)
