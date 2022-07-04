#! /usr/bin/python3

# nuggetizer.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Entrypoint of the Power Nugget client
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import Union, Optional, Generator
from copy import deepcopy
from pathlib import Path

from powernugget.deserializer import _deserialize_yaml_as
from powernugget.deserializer.models import Inventory, Tasks_list, Task
from powernugget.tasks_generator import TasksGenerator
from powernugget.errors import Errors


#############################################################################
#                                  Script                                   #
#############################################################################

Pathable = Union[str, Path]


class Nuggetizer:
    """
    Entrypoint of the Power Nugget client
    """

    def __init__(
        self,
        *,
        path: Pathable,
        inventory_file_name: Optional[Pathable] = None,
        tasks_file_name: Optional[Pathable] = None,
        dashboard_template_file_name: Optional[Pathable] = None
    ):
        """
        Initialize the Nuggetizer

        Args:
            path (Pathable): The root path of the project where the inventory and tasks files are located.
            inventory_file_name (Pathable, optional): An optional inventory file path. Defaults to "inventory.yaml".
            tasks_file_name (Pathable, optional): An optional tasks file path. Defaults to "tasks.yaml".
            dashboard_template_file_name (Pathable, optional): An optional dashboard template file. Defaults to "dashboard_template.pbit".
        """

        # Configure the paths to the artifacts
        base_path = Path(path)
        self._path = base_path
        self._inventory_file_name: Path = Path(inventory_file_name or base_path / "inventory.yaml")
        self._tasks_file_name: Path = Path(tasks_file_name or base_path / "tasks.yaml")
        self._dashboard_template_file_name: Path = Path(dashboard_template_file_name or base_path / "dashboard_template.pbit")

        # # Parse the Pyproject PowerNugget's section of the configuration
        # self._root_folder: Path = _get_path_to_target("pyproject.toml")
        # self._config: Pyproject = _get_pyproject(root_folder)

    def execute(self):
        """
        Render a dasboard template by executing the tasks against the inventory.
        """

        # Prepare the inventory and the task file to be templated
        inventory: Inventory = _deserialize_yaml_as(self._inventory_file_name, Inventory)  # type: ignore
        tasks_list: Tasks_list = _deserialize_yaml_as(self._tasks_file_name, tasks_list)  # type: ignore

        for dashboard_name, dashboard_data in inventory.dashboards.items():
            # with dashboard_..
            for task in TasksGenerator(tasks_list, dashboard_name=dashboard_name, dashboard_data=dashboard_data):
                # task.execute()
                print(task)
