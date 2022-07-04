#! /usr/bin/python3

# yaml.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Primitive for yaml deserialization against PowerNugget's models
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pathlib import Path
import yaml
from typing import Union

from pydantic import ValidationError

from powernugget.descriptions.models import Inventory, Tasks_list
from powernugget.errors import Errors

#############################################################################
#                                  Script                                   #
#############################################################################

Models = Union[Inventory, Tasks_list]


def _deserialize_yaml_as(path: Path, model: Models) -> Models:
    """
    Load, render and parse a template into a model.
    Args:
        path (Path): the path to the ressource to render.
        model (Models): the model to unmarshall.
    """

    # Load the raw template
    try:
        with open(path) as f:
            raw_template = f.read()
    except BaseException as error:
        raise Errors.E020(path=str(path)) from error  # type: ignore

    # Parse the raw_template as yaml
    try:
        parsed = yaml.safe_load(raw_template)
    except BaseException as error:
        raise Errors.E021() from error  # type: ignore

    # Unmarshal the template
    try:
        parsed_model = model.of(parsed)  # type: ignore
    except (TypeError, ValidationError) as error:
        raise Errors.E022(definition=parsed, model=type(Model)) from error  # type: ignore

    return parsed_model
