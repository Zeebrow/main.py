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

from typing import List
from dataclasses import dataclass
import argparse
from abc import ABCMeta, abstractmethod
import configparser
import logging
from pathlib import Path

from .constants import APP_CONST as C

logger = logging.getLogger(__name__)


class AppConfigFileParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__(allow_no_value=True)

class ParserBase(metaclass=ABCMeta):
    def __init__(self, config_file=C.DEFAULT_CONFIG_FILEPATH) -> None: ...

    @abstractmethod
    def add_subparsers(self, parser: argparse.ArgumentParser) -> None: ...

    @abstractmethod
    def add_init_parser_arguments(self, parser: argparse.ArgumentParser) -> None: ...

    @abstractmethod
    def add_make_parser_arguments(self, parser: argparse.ArgumentParser) -> None: ...

    @abstractmethod
    def add_describe_parser_arguments(self, parser: argparse.ArgumentParser) -> None: ...

    @abstractmethod
    def add_update_parser_arguments(self, parser: argparse.ArgumentParser) -> None: ...

    @abstractmethod
    def add_destroy_parser_arguments(self, parser: argparse.ArgumentParser) -> None: ...

class AppBase(metaclass=ABCMeta):
    def __init__(self, config_file=C.DEFAULT_CONFIG_FILEPATH):
        """should there actually be logic here? in the same vain, more than just primitive data types?"""
        self.config_file = Path(config_file).absolute()
        if not self.config_file.exists():
            raise RuntimeError(f"no such file: {self.config_file}")

    @abstractmethod
    def load_default_config(self):
        """get possible config from file"""
        ...

    @abstractmethod
    def plugin_init():
        """Account setup, networking, etc. required to use plugin"""
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
