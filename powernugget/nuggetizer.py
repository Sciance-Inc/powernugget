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
from typing import Union, Optional, Dict, List, Any
from pathlib import Path
from importlib import import_module
from copy import deepcopy

from powernugget.descriptions import _deserialize_yaml_as, _deserialize_yaml
from powernugget.descriptions.models import Inventory, Tasks_list, Task
from powernugget.tasks_generator import TaskGenerator
from powernugget.builtins.nugget import Nugget, NuggetExecutionStatus, NuggetResult
from powernugget.dashboard import Dashboard, PowerBIOpener
from powernugget.errors import Errors
from powernugget.logger import MixinLogable

#############################################################################
#                                  Script                                   #
#############################################################################

Pathable = Union[str, Path]


class Nuggetizer(MixinLogable):
    """
    Entrypoint of the Power Nugget client
    """

    def __init__(
        self,
        *,
        path: Pathable,
        inventory_file_name: Optional[Pathable] = None,
        tasks_file_name: Optional[Pathable] = None,
        vars_file_name: Optional[Pathable] = None,
        dashboard_template_file_name: Optional[Pathable] = None,
    ):
        """
        Initialize the Nuggetizer

        Args:
            path (Pathable): The root path of the project where the inventory and tasks files are located.
            inventory_file_name (Pathable, optional): An optional inventory file path. Defaults to "inventory.yaml".
            tasks_file_name (Pathable, optional): An optional tasks file path. Defaults to "tasks.yaml".
            vars_file_name (Pathable, optional): An optional vars file path. All variables will be added to the rendering context. Defaults to "vars.yaml".
            dashboard_template_file_name (Pathable, optional): An optional dashboard template file. Defaults to "dashboard_template.pbit".
        """

        super().__init__(logger_name="Nuggetizer")

        # Configure the paths to the artifacts
        base_path = Path(path)
        self._path = base_path
        self._inventory_file_name: Path = Path(inventory_file_name or base_path / "inventory.yaml")
        self._tasks_file_name: Path = Path(tasks_file_name or base_path / "tasks.yaml")
        self._vars_file_name: Path = Path(vars_file_name or base_path / "vars.yaml")
        self._dashboard_template_file_name: Path = Path(dashboard_template_file_name or base_path / "dashboard_template.pbit")

        # # Parse the Pyproject PowerNugget's section of the configuration
        # self._root_folder: Path = _get_path_to_target("pyproject.toml")
        # self._config: Pyproject = _get_pyproject(root_folder)

    def _get_nugget_class(self, fqn: str) -> Nugget:
        """
        Fetch the Nugget among the builtins modules to get the nugget class

        TODO : add support for UDN (User Defined Nugget)
        Args:
            fqn (str): The fully qualified nugget name
        """

        try:
            callable_, *modules = fqn.split(".")[::-1]
            modules = modules[::-1]
            nugget_class = getattr(
                import_module(".".join(modules)),
                callable_,
            )
        except BaseException:
            raise Errors.E030(fqn=fqn)  # type: ignore

        return nugget_class

    def _task_to_nugget(self, task: Task, dashboard: Dashboard) -> Nugget:
        """
        Transform a task to a concrete nugget
        """

        nugget_class = self._get_nugget_class(task.nugget)
        return nugget_class(dashboard=dashboard, **task.params)  # type: ignore

    def execute(self) -> Dict[str, List[NuggetResult]]:
        """
        Render a dasboard template by executing the tasks against the inventory.
        """

        # Prepare the inventory and the task file to be templated
        inventory: Inventory = _deserialize_yaml_as(self._inventory_file_name, Inventory)  # type: ignore
        tasks_list: Tasks_list = _deserialize_yaml_as(self._tasks_file_name, Tasks_list)  # type: ignore

        # Extract the vars file (if any)
        vars_: Dict[str, Any] = {}
        if self._vars_file_name.exists():
            vars_ = _deserialize_yaml(self._vars_file_name)

        # Keep a record of every nugget executed
        summary: Dict[str, List[NuggetResult]] = defaultdict(lambda: [])  # type: ignore

        # Prepare the dashboard template by unzipping it.
        # The context manager returns a callable to be called for generating an updatable copy of the Template
        with PowerBIOpener(self._dashboard_template_file_name) as opener:

            for dashboard_name, dashboard_data in inventory.dashboards.items():

                self.info(f" *** PLAY [{dashboard_name}] *** \n")

                # Create the templating magic variables
                magics = {
                    "vars": deepcopy(vars_),
                    "dashboard_name": dashboard_name,
                    "dashboard_data": dashboard_data,
                    "root_path": str(self._path),
                }

                # Create a dashboard representation to be updated by the tasks.
                # The closer callable can be executed to save the dahsboard.
                dashboard, closer = opener(dashboard_name)

                # Generate the tasks to be executed : the tasks are contextualized from the dashboard context
                for task in TaskGenerator(tasks_list, **magics):
                    self.info(f"TASK [{task.name}]")

                    # Check if the Task must be executed
                    if not task.when:
                        self.info("\033[33m Passed\033[00m\n")
                        result = NuggetResult(status=NuggetExecutionStatus.PASSED, result=None)
                        summary[dashboard_name].append(result)
                        continue

                    # If so, map the Task to a Nugget
                    nugget = self._task_to_nugget(task, dashboard)

                    # Try to execute the nugget, and set the status as a success
                    try:
                        output = nugget.run()
                        result = NuggetResult(status=NuggetExecutionStatus.SUCCESS, result=output)
                        self.info("\033[92m Ok\033[00m\n")

                    # In case of error, set the status as a failure but only raise the error if the task is mandatory
                    except BaseException as error:
                        if task.on_error != "ignore":  # todo Replace with LiteralEnum
                            raise Errors.E031(nugget_name=nugget.nugget_name, dashboard=dashboard_name) from error  # type: ignore
                        result = NuggetResult(status=NuggetExecutionStatus.FAILED, result=None)
                        self.info("\033[91m Failled\033[00m\n")

                    summary[dashboard_name].append(result)

                # Serialize the dashboard to the target folder
                closer()

        return summary
