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
    def __init__(self, config_file=C.DEFAULT_CONFIG_FILEPATH):
        pass

    @abstractmethod
    def add_parser_arguments(self, action: str, parser: argparse.ArgumentParser) -> None:
        pass

class AppBase(metaclass=ABCMeta):
    def __init__(self, config_file=C.DEFAULT_CONFIG_FILEPATH):
        """should there actually be logic here? in the same vain, more than just primitive data types?"""
        self.config_file = Path(config_file).absolute()
        if not self.config_file.exists():
            raise RuntimeError(f"no such file: {self.config_file}")

    @abstractmethod
    def load_default_config(self):
        """get possible config from file"""
        pass

    @abstractmethod
    def plugin_init():
        """Account setup, networking, etc. required to use plugin"""
        pass

    @abstractmethod
    def create(self):
        """
        Start hosts
        """
        pass

    @abstractmethod
    def describe(self) -> dict:
        """return information about hosts in the target app"""
        pass

    @abstractmethod
    def update(self):
        """change the hosts in some way"""
        pass
        
    @abstractmethod
    def destroy(self):
        """ delete all hosts associated with your app """
        pass
