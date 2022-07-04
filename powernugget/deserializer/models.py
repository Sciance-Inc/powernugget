#! /usr/bin/python3

# configurations.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Configurations related models
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import Optional, Dict, Any, List, Union
from pydantic import Field, BaseModel, Extra
from pydantic.dataclasses import dataclass


#############################################################################
#                                  Script                                   #
#############################################################################


@dataclass
class Pyproject:
    """
    Pyproject model configurations definition
    """

    custom_nuggets_repo: Optional[str]


# Pydantic.dataclasses does not support the extra config class, so we need to use a BaseModel instead
class Inventory(BaseModel, extra=Extra.ignore):
    """
    Inventory model configurations definition
    """

    dashboards: Dict[str, Dict[str, Any]]

    @staticmethod
    def of(raw_str):
        return Inventory(**raw_str)


@dataclass
class Task:
    """
    A single Task definition
    """

    name: str
    nugget: str
    params: Optional[Dict[str, Any]] = None
    loop: Optional[str] = None
    loop_key: Optional[str] = "item"
    when: Optional[Union[bool, str]] = None
    register_out: Optional[str] = Field(None, alias="register")
    # Register is actually a reserved keyword. I alias it to register_out to keep the code consistent with Ansible


@dataclass
class Tasks_list:
    """
    Tasks model configurations definition
    """

    tasks: List[Task]

    @staticmethod
    def of(raw_str):
        return Tasks_list(tasks=raw_str)
