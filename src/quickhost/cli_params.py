from typing import List
from dataclasses import dataclass
from argparse import Namespace, SUPPRESS
from abc import ABCMeta, abstractmethod
import configparser
import logging
from os import get_terminal_size

from .utilities import get_my_public_ip
from .constants import *

logger = logging.getLogger(__name__)

class AppConfigFileParser(configparser.ConfigParser):
    """
    example config file:
    [aws:_all]
    key_name = my-ec2-key
    vpc_id = vpc-1234
    subnet_id = subnet-23414516134

    [aws:app1]
    # apps override '_all'
    key_name = my-special-app-key
    """
    def __init__(self):
        super().__init__(allow_no_value=True)

@dataclass(init=True)
class AppCLIParams:
    app_name: str
    userdata: str = None
    ami: str = None
    num_hosts: int = 1
    instance_type: str = 't2.micro'
    userdata: str = None
    ports: List[int] = None 
    cidrs: List[str] = None
    dry_run: bool = True


class ConfigBase(metaclass=ABCMeta):
    def __init__(self, _cli_parser_id: str, app_name: str, config_file=DEFAULT_CONFIG_FILEPATH):
        self._cli_parser_id = _cli_parser_id
        self.app_name = app_name
        self.config_file = Path(config_file).absolute()
        if not self.config_file.exists():
            raise RuntimeError(f"no such file: {self.config_file}")
        if self._cli_parser_id is None:
            raise Exception("need a cli_parser_id")

    @abstractmethod
    def load_default_config(self):
        """get possible config from file"""
        pass

    @abstractmethod
    def load_cli_args(self):
        """get remaining config from argparse namespace"""
        pass

    @classmethod
    @abstractmethod
    def parser_arguments(self, subparsers: any) -> None:
        """modify main ArgumentParser to accept these arguments"""
        pass


    @abstractmethod
    def print_loaded_args(self) -> None:
        pass

    @abstractmethod
    def create(self):
        """do the needful to get app up"""
        pass

    @abstractmethod
    def destroy(self):
        """do the needful to tear app down"""
        pass
        
class App(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        """do the needful to get app up"""
        pass

    @abstractmethod
    def destroy(self):
        """do the needful to tear app down"""
        pass
