#! /usr/bin/python3

# pbit.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
A PowerBI Opener : to open and load the data from a powerbi template, implemented as context manager
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import Dict, Any
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
from copy import deepcopy
import json

from powernugget.errors import Errors
from powernugget.dashboard import Dashboard

#############################################################################
#                                  Script                                   #
#############################################################################

_DATA_MODEL = "DataModelSchema"
_LAYOUT = "Report/Layout"
_PBIT_ENCODING = "UTF-16 LE"


def _load_json(src, encoding="utf-8") -> Dict[str, Any]:
    """
    Load a json file and return the content as a dictionary
    """

    with open(src, "r", encoding=encoding) as f:
        return json.load(f)


class PowerBIOpener:
    """
    A context manager to open a PowerBI dashboard
    """

    def __init__(self, path: Path):
        """
        Unzip the Dashboard into a tempfile
        """

        extension = path.suffix
        if extension != ".pbit":
            raise Errors.E040(extension=extension)  # type: ignore

        self._path = path
        self._src_path: Path

    def __enter__(self):
        """
        Deserialize the dashboard into a temp folder
        """

        # All transformations schould happen in the temp folder
        self._temp_dir = TemporaryDirectory()

        # Unzip the dashboard into the temp folder
        self._src_path = Path(str(self._temp_dir.name)) / "src"
        try:
            shutil.unpack_archive(self._path, self._src_path, format="zip")
        except shutil.ReadError:
            raise Errors.E041(path=self._path)  # type: ignore
        except BaseException as error:
            raise Errors.E041(path=self._path) from error  # type: ignore

        # Load the dashboard data, to be reused accross iteration
        data = _load_json(self._src_path / _DATA_MODEL, encoding=_PBIT_ENCODING)
        layout = _load_json(self._src_path / _LAYOUT, encoding=_PBIT_ENCODING)

        # Create a closure to be called to regenerate a new dashboard
        def _(dashboard_name: str) -> Dashboard:
            """
            Create a Dahsboard to be updated
            """

            # The unpacked dashboard for this iteration is kept inside the top level temp dir to be GC / cleanup at the same time
            dst = Path(self._temp_dir.name) / dashboard_name

            # Copy the source dashboard into the temp folder
            shutil.copytree(self._src_path, dst)

            return Dashboard(path=dst, data_model=deepcopy(data), layout=deepcopy(layout))

        return _

    def __exit__(self, exc_type, exc_value, traceback):

        self._temp_dir.cleanup()
        return True
