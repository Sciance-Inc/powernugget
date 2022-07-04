#! /usr/bin/python3

# test_tasks_generator.py
#
# Project name: Power Nugget
# Author: Hugo Juhel
#
# description:
"""
    Test the way the tasks generator and parsing works
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

import pytest
from pathlib import Path

from powernugget.deserializer import _deserialize_yaml_as
from powernugget.deserializer.models import Inventory, Tasks_list


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


def test_simple_inventory_loading():
    """
    Check if the Nuggetizer is able to fetch and parse the Inventory
    """

    p = Path("tests/test_repo/").absolute() / "inventory.yaml"
    inventory: Inventory = _deserialize_yaml_as(p, Inventory)  # type: ignore

    target = {"color_remapping": {"outer": {"from": "red", "to": "bleu"}, "inner": {"from": "red iner", "to": "bleu inner"}}}
    assert inventory.dashboards["cssvdc"] == target


def test_simple_tasks_list_loading():
    """
    Check if the Nuggetizer is able to fetch and parse the tasks list
    """

    p = Path("tests/test_repo/").absolute() / "tasks.yaml"
    tasks_list: Tasks_list = _deserialize_yaml_as(p, Tasks_list)  # type: ignore

    task = tasks_list.tasks[0]

    assert task.nugget == "powernugget.builtins.debug"
