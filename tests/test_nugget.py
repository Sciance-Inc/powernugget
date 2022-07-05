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


from pathlib import Path
from powernugget.builtins.nugget import NuggetResult, NuggetExecutionStatus

#############################################################################
#                                   Script                                  #
#############################################################################


def test_debug_nugget(caplog):

    from powernugget.builtins import Debug
    from powernugget.dashboard import Dashboard

    dashboard = Dashboard(path=Path("."), data_model={}, layout={})
    nugget = Debug(dashboard=dashboard, msg="Hello world")
    result = nugget.run()
    # assert "" in caplog.text  # TO DO fix the test as the log is not currently not captured
