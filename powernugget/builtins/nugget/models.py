#! /usr/bin/python3

# models.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Nugget execution'S result wrappers
"""

#############################################################################
#                                 Packages                                  #
#############################################################################


from typing import Dict, Any
from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass

from powernugget.dashboard import Dashboard

#############################################################################
#                                  Script                                   #
#############################################################################


class NuggetExecutionStatus(Enum):
    """
    The nugget execution status
    """

    SUCCESS = 1
    FAILED = 2
    PASSED = 3


@dataclass
class NuggetResult:
    """
    The result of a Nugget execution
    """

    status: NuggetExecutionStatus
    result: Dict[str, Any] = Field(default_factory=dict())  # type: ignore
