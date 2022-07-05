#! /usr/bin/python3

# nugget.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
The Nugget interface that must be implemented by any nugget
"""

#############################################################################
#                                 Packages                                  #
#############################################################################


from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Any

from powernugget.dashboard import Dashboard

#############################################################################
#                                  Script                                   #
#############################################################################


class Nugget(metaclass=ABCMeta):
    """
    Define the Interface that must be implemented by any nugget
    """

    @abstractmethod
    def __init__(self, dashboard: Dashboard, *args, **kwargs):
        """
        Instanciate the nugget

        Args:
            dashboard (Dashboard): The Dashboard representation to apply the nugget to
        """

        super().__init__(*args, **kwargs)
        self._dashboard = dashboard

    @abstractproperty
    def nugget_name(self) -> str:
        """
        The friendly name of the nugget
        """

        raise NotImplementedError("Must be implemented by the derived Nugget")

    @abstractmethod
    def run(self) -> Any:
        """
        Run the nugget
        """

        raise NotImplementedError("Must be implemented by the derived Nugget")
