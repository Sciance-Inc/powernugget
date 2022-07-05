#! /usr/bin/python3

# change_image.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
The ChangeImage nugget replace a image in the dashboard
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pathlib import Path
from shutil import copyfile
from powernugget.builtins.nugget import Nugget
from powernugget.dashboard import Dashboard
from powernugget.logger import MixinLogable

#############################################################################
#                                  Script                                   #
#############################################################################


class ReplaceImage(Nugget, MixinLogable):
    """
    The ReplaceImage nugget replace a image in the dashboard
    """

    nugget_name: str = "replace_image"

    def __init__(self, *, dashboard: Dashboard, source_name: str, target_path: str):
        """
        Replace the image identified by source_name with the image located at target_path

        Args:
            dashboard (Dashboard): The dashboard object to apply the nugget to
            source_name (str): The source name, as defined in the unzipped template
            target_path (str): The path / to the new ressource.
        """

        super().__init__(logger_name=ReplaceImage.nugget_name, dashboard=dashboard)
        self._source_name = source_name
        self._target_path = target_path

    def run(self):
        """
        Replace the image
        """

        # Build the two paths
        destination_path = self._dashboard.path / "Report" / "StaticResources" / "RegisteredResources" / self._source_name
        if not destination_path.exists:
            raise ValueError(f'The source image "{destination_path}" does not exist in the dashboard template')

        target_path = Path(self._target_path).resolve().absolute()
        if not target_path.exists:
            raise ValueError(f'The target image "{target_path}" does not exist in the dashboard template')

        copyfile(target_path, destination_path)
