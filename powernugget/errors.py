#! /usr/bin/python3

# errors.py
#
# Project name: power nugget
# Author: Hugo Juhel
#
# description:
"""
Centralize errors for the powernugget package
"""

# pylint: disable-all
#############################################################################
#                                 Packages                                  #
#############################################################################

# System packages
import sys
import warnings

# Project related packages
from .logger import get_module_logger

#############################################################################
#                                Constants                                  #
#############################################################################

DEFAULT_LOGGER = get_module_logger(__name__)
PROJECT_NAME = "PowerNugget"

#############################################################################
#                                 Classes                                   #
#############################################################################


class ExceptionFactory(type):
    """
    Implements a metaclass building errors from instances attributes. Errors are singleton and can be raised and catched.

    >>raise Errors.E010
    >>raise Errors.E010()
    """

    def __init__(cls, name, bases, attrs, *args, **kwargs):
        super().__init__(name, bases, attrs)
        super().__setattr__("_instance", None)
        super().__setattr__("_CACHED_ATTRIBUTES", dict())

    def __call__(cls, *args, **kwargs):
        if super().__getattribute__("_instance") is None:
            super().__setattr__("_instance", super().__call__(*args, **kwargs))
        return super().__getattribute__("_instance")

    def __getattribute__(cls, code):
        """
        Intercept the attribute getter to wrap the Error code in a metaclass. By doing so, the error code became
        a proper class for which the name is the error code
        """

        try:
            meta = super().__getattribute__("_CACHED_ATTRIBUTES")[code]
        except KeyError:

            # Retrieve the error message maching the code and preformat it
            msg = super().__getattribute__(code)
            msg = f"{PROJECT_NAME} : {code} - {msg}"

            proto = super().__getattribute__("_PROTOTYPE")
            meta = type(code, (proto,), {"msg": msg})
            super().__getattribute__("_CACHED_ATTRIBUTES")[code] = meta

        return meta


class ErrorPrototype(Exception):
    """
    Base parent for all custom errors raised by the program.
    The class performs base operation making the error message displaybale
    """

    msg: str = ""

    def __init__(self, **kwargs):

        super().__init__(self.msg.format(**kwargs))


class WarningPrototype(UserWarning):
    """
    Base parent for all custom warnings raised by the program.
    The class performs base operation making the warning displayba;e
    """

    msg: str = ""

    def __init__(self, **kwargs):

        super().__init__(self.msg.format(**kwargs))


class Errors(metaclass=ExceptionFactory):  # type: ignore

    _PROTOTYPE = ErrorPrototype

    # Init and connection related errors
    E010 = "start-up : PowerNugget must be called from a folder, or the child of a folder, containing a '{target}' file / folder."
    E011 = "start-up : failed to open the pyproject.toml file at '{path}'."
    E012 = "start-up : the pyproject.toml powernugget's section is missing a mandatory field."

    # Templating related errors
    E020 = "templating : failed to load the template at '{path}'."
    E021 = "templating : the loaded yaml is not valid."
    E022 = "templating : the following definition is not a valid '{model}' : \n{definition}."

    # Nuggetizer related errors
    E030 = "nuggetizer: failed to import the '{fqn}'. Does the nugget exist in the builtins env ?"
    E031 = "nuggetizer: failed to execute the '{nugget_name}' nugget for dashboard : {dashboard}."

    # Dashboard content errors
    E040 = "powerOpener : the dashboard template schould be a '.pbit' file. Got '{extension}'"
    E041 = "powerOpener : failed to unpack the template '{path}' into a temporary folder."
    E042 = "powerOpener : the template '{path}' does not seems to exist, or is not a valid zip file."


class Warnings(UserWarning):

    _PROTOTYPE = WarningPrototype

    # Instanciation
    W010 = "bar"


def _custom_formatwarning(msg, *args, **kwargs) -> str:
    """
    Monkey patch the warning displayor to avoid printing the code longside the Warnings.
    Monkeypatching the formatter is acutalyy the way to do it as recommanded by Python's documention.
    """
    return f"Warning : {str(msg)} \n"


warnings.formatwarning = _custom_formatwarning


if __name__ == "__main__":
    sys.exit()
