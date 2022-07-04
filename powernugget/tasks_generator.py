#! /usr/bin/python3

# tasks_generator.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Implements the task rendering logic
"""

#############################################################################
#                                 Packages                                  #
#############################################################################


from ast import literal_eval
from typing import Any, Generator, List, Union, Dict
from copy import deepcopy
from functools import singledispatch

from jinja2 import Template

from powernugget.descriptions.models import Tasks_list, Task
from powernugget.errors import Errors


#############################################################################
#                                  Script                                   #
#############################################################################


@singledispatch
def _render(src: Union[str, Dict, List], ctx: Dict[str, Any]):
    """
    Jinja2-render any yaml structure with a provided context.

    Args:
        src (Union[str, Dict, List]): The yaml structure to be templated
        ctx (Dict[str, Any]): The rendering vars context
    """

    raise ValueError(f"Unsupported type {type(src)}")


@_render.register(type(None))
def _(src: None, ctx: Dict[str, Any]):
    return None


@_render.register(str)
def _(src, ctx) -> str:
    return Template(src).render(**ctx) or ""


@_render.register(list)
def _(src, ctx) -> List[str]:
    return [_render(item, ctx) for item in src]


@_render.register(dict)
def _(src, ctx) -> Dict[str, Any]:
    return {key: _render(value, ctx) for key, value in src.items()}


class TaskGenerator:
    """
    Implements the task rendering logic
    """

    def __init__(self, tasks_list: Tasks_list, **initial_context):
        self._tasks_list = tasks_list
        self._initial_context = deepcopy(initial_context)  # As we are iterating over the tasks, we need to update the context

    def __iter__(self) -> Generator[Task, None, None]:
        """
        Implements the iterator protocol.
        Render a tasks_list into a generator of tasks
        """

        def _():
            for task in self._tasks_list.tasks:
                if task.loop:
                    rendered_tasks = self._render_task_loop(task)
                else:
                    rendered_tasks = (self._render_task(task, self._initial_context),)

                for task in rendered_tasks:
                    yield task

        return _()

    def _render_task_loop(self, task) -> Generator[Task, None, None]:
        """
        Expand a loop condition to render multiples tasks
        """

        # First render and parse the looping condition
        loop = _render(task.loop, self._initial_context)
        loop = literal_eval(loop)

        # Return a generator looping over each local task
        def _():

            # Each iterations has it's own context, we need to update it with the loop item
            for item in loop:
                this_iteration_context = deepcopy(self._initial_context)
                this_iteration_context[task.loop_key] = item
                yield self._render_task(task, this_iteration_context)

        return _()

    def _render_task(self, task: Task, context) -> Task:
        """
        Render a task with a rendering context
        """

        name = _render(task.name, context)
        nugget = _render(task.nugget, context)
        when = _render(task.when, context)
        params = _render(task.params, context)
        register_out = _render(task.register_out, context)

        # Pseudo-safe eval context for the when rendering
        when = eval(when, context) if when else True

        return Task(name=name, nugget=nugget, params=params, when=when, register_out=register_out)  # type: ignore
