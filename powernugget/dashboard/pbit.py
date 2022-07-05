#! /usr/bin/python3

# pbit.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# Found usefull ressources here : https://www.reddit.com/r/PowerBI/comments/tj98fs/is_there_any_way_of_editing_the_layout_file/
# description:
"""
A PowerBI Opener : to open and load the data from a powerbi template, implemented as context manager
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

import os
from typing import Dict, Any, Callable, Tuple
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
_PBIT_ENCODING = "utf-16-le"
_XML_ENCODING = "utf-8"


def _load_json(src) -> Dict[str, Any]:
    """
    Load a json file and return the content as a dictionary
    """

    with open(src, "r", encoding=_PBIT_ENCODING) as f:
        return json.load(f)


def _dump_json(trg, payload: Dict[str, Any]) -> None:
    """
    Save a payload as a json file
    """

    with open(trg, "w", encoding=_PBIT_ENCODING) as f:
        json.dump(payload, f)


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

        self._src_template_path = path
        self._destination_basepath = path.parent
        self._src_path: Path

    def __enter__(self):
        """
        Deserialize the dashboard into a temp folder
        """

        # All transformations schould happen in the temp folder
        self._temp_dir = TemporaryDirectory()

        # Unzip the dashboard into the temp folder
        self._unzipped_template_path = Path(str(self._temp_dir.name)) / "src"
        try:
            shutil.unpack_archive(self._src_template_path, self._unzipped_template_path, format="zip")
        except shutil.ReadError:
            raise Errors.E041(path=self._src_template_path)  # type: ignore
        except BaseException as error:
            raise Errors.E041(path=self._src_template_path) from error  # type: ignore

        # Remove the SecurityBinding file
        os.remove(self._unzipped_template_path / "SecurityBindings")

        # Load the dashboard data, to be reused accross iteration
        data = _load_json(self._unzipped_template_path / _DATA_MODEL)
        layout = _load_json(self._unzipped_template_path / _LAYOUT)

        # Create a closure to be called to regenerate a new dashboard
        def _(dashboard_name: str) -> Tuple[Dashboard, Callable]:
            """
            Create a Dahsboard to be updated
            """

            # The unpacked dashboard for this iteration is kept inside the top level temp dir to be GC / cleanup at the same time
            tmp_dashboard_path = Path(self._temp_dir.name) / dashboard_name

            # Copy the source dashboard into the temp folder
            shutil.copytree(self._unzipped_template_path, tmp_dashboard_path)

            # Create a dashboard with the data and layout
            dashboard = Dashboard(path=tmp_dashboard_path, data_model=deepcopy(data), layout=deepcopy(layout))

            # Create a closure to be called for closing the dashboard
            def close():
                # Save the dashboard data
                _dump_json(tmp_dashboard_path / _DATA_MODEL, dashboard.data_model)
                _dump_json(tmp_dashboard_path / _LAYOUT, dashboard.layout)

                # Zip the archive to the target path
                out = Path(shutil.make_archive(str(self._destination_basepath / dashboard_name), "zip", tmp_dashboard_path))

                # Replace the zip extension with the pbit extension
                os.rename(out, out.parent / (out.stem + ".pbit"))

            return dashboard, close

        return _

    def __exit__(self, exc_type, exc_value, traceback):

        self._temp_dir.cleanup()
        return True
