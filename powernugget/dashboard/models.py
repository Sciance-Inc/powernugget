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
import json
import shutil

#############################################################################
#                                  Script                                   #
#############################################################################

_DATA_MODEL = "DataModelSchema"
_LAYOUT = "Report/Layout"
_PBIT_ENCODING = "UTF-16 LE"


def _dump_json(trg, payload: Dict[str, Any]) -> None:
    """
    Load a json file and return the content as a dictionary
    """

    with open(trg, "rw", encoding=_PBIT_ENCODING) as f:
        f.truncate()
        json.dump(payload, f)


@dataclass
class Dashboard:
    """
    The Dashboard representation
    """

    path: Path
    data_model: Dict[str, Any]
    layout: Dict[str, Any]
