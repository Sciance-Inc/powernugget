#! /usr/bin/python3

# test_tasks_generator.py
#
# Project name: Power Nugget
# Author: Hugo Juhel
#
# description:
"""
    Test that builtins nuggets work
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import List, Dict
from pathlib import Path
import pytest
from powernugget.builtins.nugget import NuggetResult, NuggetExecutionStatus


#############################################################################
#                                   Script                                  #
#############################################################################


@pytest.fixture
def ngtz():
    """
    Create a Nuggetizer instance
    """

    from powernugget import Nuggetizer

    p = Path("tests/test_repo/").absolute()

    return Nuggetizer(path=p)


def test_nuggetizer_execute(ngtz):

    summary: Dict[str, List[NuggetResult]] = ngtz.execute()

    results = [item for v in summary.values() for item in v]

    assert results[0].status == NuggetExecutionStatus.SUCCESS
