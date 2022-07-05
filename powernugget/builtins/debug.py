#! /usr/bin/python3

# models.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
The Debug nugget echo a message to the standard output
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from powernugget.builtins.nugget import Nugget, NuggetResult, NuggetExecutionStatus
from powernugget.dashboard import Dashboard

#############################################################################
#                                  Script                                   #
#############################################################################


class Debug(Nugget):
    """
    The Debug nugget echo a message to the standard output
    """

    nugget_name: str = "debug_nugget"

    def __init__(self, *, dashboard: Dashboard, msg: str):
        super().__init__(dashboard=dashboard)
        self._msg = msg

    def run(self) -> NuggetResult:
        """
        Print the message
        """

        print(self._msg)
        return NuggetResult(status=NuggetExecutionStatus.SUCCESS, result={})
