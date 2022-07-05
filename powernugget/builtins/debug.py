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

from powernugget.builtins.nugget import Nugget
from powernugget.dashboard import Dashboard
from powernugget.logger import MixinLogable

#############################################################################
#                                  Script                                   #
#############################################################################


class Debug(Nugget, MixinLogable):
    """
    The Debug nugget echo a message to the standard output
    """

    nugget_name: str = "debug_nugget"

    def __init__(self, *, dashboard: Dashboard, msg: str):
        super().__init__(logger_name=Debug.nugget_name, dashboard=dashboard)
        self._msg = msg

    def run(self):
        """
        Print the message
        """

        self.debug(self._msg)
