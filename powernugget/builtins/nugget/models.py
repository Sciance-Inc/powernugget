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


from typing import Optional, Any
from enum import Enum
from pydantic.dataclasses import dataclass

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
    result: Optional[Any] = None  # type: ignore
