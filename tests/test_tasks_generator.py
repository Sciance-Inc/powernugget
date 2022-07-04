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
from powernugget.tasks_generator import TasksGenerator
from powernugget.deserializer import _deserialize_yaml_as
from powernugget.deserializer.models import Tasks_list

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


def test_looping_task_generator():
    """
    Check if the task generator is able to render loops of tasks
    """

    p = Path("tests/test_repo/").absolute() / "tasks.yaml"
    tasks_list: Tasks_list = _deserialize_yaml_as(p, Tasks_list)  # type: ignore

    G = TasksGenerator(
        tasks_list,
        dashboard_name="cssvdc",
        dashboard_data={"color_remapping": {"outer": {"from": "red", "to": "bleu"}, "inner": {"from": "red inner", "to": "bleu inner"}}},
    )

    tasks = [item for item in G]

    assert tasks[0].params["msg"] == "Replacing red with bleu"  # type: ignore
    assert tasks[1].params["msg"] == "Replacing red inner with bleu inner"  # type: ignore
    assert tasks[1].when is True
    assert tasks[2].params["msg"] == "Doing non parametric stuff on cssvdc"  # type: ignore
    assert tasks[2].when is False  # type: ignore
