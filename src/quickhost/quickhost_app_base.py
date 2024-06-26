# Copyright (C) 2022 zeebrow

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from abc import abstractmethod, abstractclassmethod
import logging

logger = logging.getLogger(__name__)


class ParserBase():
    """
    A plugin's __init__.py must implement a function named get_parser() which return the implementation of this class.
    """
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def add_subparsers(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abstractmethod
    def add_init_parser_arguments(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abstractmethod
    def add_make_parser_arguments(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abstractmethod
    def add_describe_parser_arguments(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abstractmethod
    def add_update_parser_arguments(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abstractmethod
    def add_destroy_parser_arguments(self, parser: argparse.ArgumentParser) -> None:
        ...


class AppBase():
    """
    The idea is to use a class as a place to stuff your CLI arguments.

    This way, you can implement a method and assign the results of AWS functions to this class' properties for reuse.

    Using the `app_name` as a key, caching may be implemented.
    """
    @abstractmethod
    def __init__(self, app_name: str):
        ...

    @abstractmethod
    def plugin_init(self):
        """Account setup, networking, etc. required to use plugin"""
        ...

    @abstractmethod
    def plugin_destroy(self):
        """ delete all resources associated with the plugin"""
        ...

    @abstractmethod
    def create(self):
        """ Start hosts """
        ...

    @abstractmethod
    def describe(self) -> dict:
        """return information about hosts in the target app"""
        ...

    @abstractmethod
    def update(self):
        """change the hosts in some way"""
        ...

    @abstractmethod
    def destroy(self):
        """ delete all hosts associated with your app """
        ...

    @abstractclassmethod
    def list_all(cls):
        """ list a plugins running app hosts """
        ...

    @abstractclassmethod
    def destroy_all(cls):
        """ list a plugins running app hosts """
        ...
