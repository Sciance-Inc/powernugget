#! /usr/bin/python3

# models.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
A dashboard representation
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

#############################################################################
#                                  Script                                   #
#############################################################################


@dataclass
class Dashboard:
    """
    The Dashboard representation
    """

    path: Path
    data_model: Dict[str, Any]
    layout: Dict[str, Any]
