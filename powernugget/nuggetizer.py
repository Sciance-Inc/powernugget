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

from collections import defaultdict
from typing import Union, Optional, Dict, List
from pathlib import Path

from powernugget.descriptions import _deserialize_yaml_as
from powernugget.descriptions.models import Inventory, Tasks_list, Task
from powernugget.tasks_generator import TaskGenerator
from powernugget.builtins.nugget import Nugget, NuggetExecutionStatus, NuggetResult
from powernugget.dashboard import Dashboard, PowerBIOpener
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

    def _task_to_nugget(self, task: Task, dashboard: Dashboard) -> Nugget:
        """
        Transform a task to a concrete nugget
        """

        from powernugget.builtins import Debug

        return Debug(dashboard=dashboard, **task.params)  # type: ignore

    def execute(self) -> Dict[str, List[NuggetResult]]:
        """
        Render a dasboard template by executing the tasks against the inventory.
        """

        # Prepare the inventory and the task file to be templated
        inventory: Inventory = _deserialize_yaml_as(self._inventory_file_name, Inventory)  # type: ignore
        tasks_list: Tasks_list = _deserialize_yaml_as(self._tasks_file_name, Tasks_list)  # type: ignore

        # Keep a record of every nugget executed
        summary: Dict[str, List[NuggetResult]] = defaultdict(lambda: [])  # type: ignore

        # Prepare the dashboard template by unzipping it.
        # The context manager returns a callable to be called for generating an updatable copy of the Template
        with PowerBIOpener(self._dashboard_template_file_name) as opener:

            for dashboard_name, dashboard_data in inventory.dashboards.items():

                # Create a dashboard representation to be updated by the tasks.
                # The closer callable can be executed to save the dahsboard.
                dashboard, closer = opener(dashboard_name)

                # Generate the tasks to be executed : the tasks are contextualized from the dashboard context
                for task in TaskGenerator(tasks_list, dashboard_name=dashboard_name, dashboard_data=dashboard_data):
                    if not task.when:
                        continue

                    # Apply the nuggets to the dashboard and store the result
                    nugget = self._task_to_nugget(task, dashboard)
                    result = nugget.run()
                    summary[dashboard_name].append(result)
                    if result.status != NuggetExecutionStatus.SUCCESS:
                        raise Errors.E030(nugget_name=nugget.nugget_name, dashboard=dashboard_name)  # type: ignore

                # Serialize the dashboard to the target folder
                closer()

        return summary
