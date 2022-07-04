#! /usr/bin/python3

# yaml_utils.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Primitive for yaml deserialization agains PowerNugget's models
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pathlib import Path
from typing import Union
from pydantic import ValidationError
import tomli


from powernugget.descriptions.models import Pyproject
from powernugget.errors import Errors

#############################################################################
#                                  Script                                   #
#############################################################################

Pathable = Union[Path, str]


def _get_path_to_target(target: str) -> Path:
    """
    Retrieve the path to "target" file by executing a "fish pass ;)" from the location of the caller
    """

    # Retrieve the "statisfactory.yaml" file
    root = Path("/")
    trg = Path().resolve()
    while True:
        if (trg / target).exists():
            return trg
        trg = trg.parent
        if trg == root:
            raise Errors.E010(target=target)  # type: ignore


def _get_pyproject(path: Pathable) -> Pyproject:
    """
    Open and validate the statisfactory section of the pyproject.toml file
    """

    path = Path(path) if Path(path).stem == "pyproject" else Path(path) / "pyproject.toml"

    # Extract the stati section from the pyproject
    try:
        with open(path, "rb") as f:
            pyproject_toml = tomli.load(f)
            config = pyproject_toml.get("tool", {}).get("powernugget", {})
    except BaseException as error:
        raise Errors.E011(path=path) from error  # type: ignore

    # Validate the config
    try:
        config = Pyproject(**config)
    except (TypeError, ValidationError) as error:
        raise Errors.E012() from error  # type: ignore

    return config
