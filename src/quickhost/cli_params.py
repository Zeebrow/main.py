from typing import List
from dataclasses import dataclass
from argparse import Namespace, SUPPRESS
from abc import ABCMeta, abstractmethod
import configparser
import logging

from .utilities import get_my_public_ip
from .constants import *

logger = logging.getLogger(__name__)

class AppConfigFileParser(configparser.ConfigParser):
    """
    example config file:
    [_app]
    invert_dryrun_flag = True
    tag_key_delimiter = :

    [AWS:_all]
    key_name = my-ec2-key
    vpc_id = vpc-1234
    subnet_id = subnet-23414516134

    [AWS:app1]
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

        
class AWSConfig(ConfigBase):
    def __init__(self, app_name, config_file=DEFAULT_CONFIG_FILEPATH):
        super().__init__('aws', app_name, config_file)
        self._config_file_parser = AppConfigFileParser()
        self._config_file_parser.read(self.config_file)
        self.userdata = None
        self.key_name = None
        self.ami = None
        self.num_hosts = None
        self.instance_type = None
        self.userdata = None
        self.ports = []
        self.cidrs = []
        self.dry_run = None
        self.vpc_id = None
        self.subnet_id = None
        self.load_default_config()

    def _all_cfg_key(self):
        return f'{self._cli_parser_id}:_all'

    def _app_cfg_key(self):
        return f'{self._cli_parser_id}:{self.app_name}'

    def load_default_config(self):
        """read values from config file, and import the relevant ones"""
        try:
            all_config = self._config_file_parser[self._all_cfg_key()]
        except KeyError:
            logger.debug(f"No '_all' config ({self._all_cfg_key()}) found in config file '{self.config_file}'")
            all_config = None
        try:
            app_config = self._config_file_parser[self._app_cfg_key()]
        except KeyError:
            logger.debug(f"No app config ({self._app_cfg_key()}) found in config file '{self.config_file}'")
            app_config = None
        print(all_config == None)
        print(app_config == None)
        for section in self._config_file_parser.sections():
            if (section.split(':')[0] == self._cli_parser_id) and (section.split(':')[1] == '_all'):
                logging.debug('found section _all')
                for k in self._config_file_parser[self._all_cfg_key()]:
                    if k in self.__dict__.keys():
                        self.__dict__[k] = self._config_file_parser[self._all_cfg_key()][k]
                    else:
                        logger.warning(f"Ignoring bad param in config: '{k}'")
            if (section.split(':')[0] == self._cli_parser_id) and (section.split(':')[1] == self.app_name):
                logging.debug(f'found section {self.app_name}')
                for k in self._config_file_parser[self._app_cfg_key()]:
                    if (k in self.__dict__.keys()) and (not k.startswith('_')):
                        self.__dict__[k] = self._config_file_parser[self._app_cfg_key()][k]
                    else:
                        logger.warning(f"Ignoring bad param in config: '{k}'")

    @classmethod
    def parser_arguments(self, subparser: any) -> None:
        aws_subparser = subparser.add_parser('aws')
        aws_subparser.add_argument("-n", "--app-name", required=True, help="Name the group of hosts you're creating (remember, there is no state!)")
        aws_subparser.add_argument("-y", "--dry-run", required=False, action='store_true', help="prevents any resource creation when set")
        aws_subparser.add_argument("-c", "--host-count", required=False, default=1, help="number of hosts to create")
        aws_subparser.add_argument("-p", "--port", required=False, type=int, action='append', default=[22], help="add an open tcp port to security group, applied to all ips")
        aws_subparser.add_argument("--ip", required=False, action='append', help="additional ipv4 to allow through security group. all ports specified with '--port' are applied to all ips specified with --ip if a cidr is not included, it is assumed to be /32")
        aws_subparser.add_argument("--instance-type", required=False, default="t2.micro", help="change the type of instance to launch")
        aws_subparser.add_argument("--ami", required=False, default=None, help="change the ami to launch, see source-aliases for getting lastest")
        aws_subparser.add_argument("-u", "--userdata", required=False, default=None, help="path to optional userdata file")
        aws_subparser.add_argument("--vpc-id", required=False, default=None, help="specify a VpcId to choose the vpc in which to launch hosts")
        aws_subparser.add_argument("--subnet-id", required=False, default=None, help="specify a SubnetId to choose the subnet in which to launch hosts")
        aws_subparser.add_argument("--key-name", required=False, default=None, help="specify the name of an EC2 keypair to use for accessing hosts")

    def check_config_for_app_name(self):
        self._config_file_parser[self._app_cfg_key()]
        pass

    def load_cli_args(self, ns: Namespace):
        """eats what parser_arguments() sets up, overriding load_default_config() values"""
        flags = vars(ns).keys()

        # dryrun
        if 'dry_run' in flags:
            self.dry_run = ns.dry_run
        else:
            self.dry_run = True

        # num hosts
        if 'host_count' in flags:
            self.num_hosts = ns.host_count
    

        # should ports and cidrs *really* overwrite config?
        # ports ingress
        # get rid of duplicates
        _ports = list(dict.fromkeys(ns.port))
        ports = []
        for p in _ports:
            # pretend they're all inst for now
            try:
                ports.append(int(p))
            except ValueError:
                raise RuntimeError("port numbers must be digits")
        self.ports = ports

        # cidrs ingress
        if not ns.ip:
            self.cidrs = [get_my_public_ip()]
        else:
            for i in ns.ip:
                if len(i.split('/')) == 1:
                    logger.warning(f"Assuming /32 cidr for ip '{i}'")
                    self.cidrs.append(i + "/32")
                else:
                    self.cidrs.append(i)

        # userdata
        if ns.userdata:
            if not Path(ns.userdata).exists():
                raise RuntimeError(f"path to userdata '{ns.userdata}' does not exist!")
            self.userdata = ns.userdata
        else:
            self.userdata = None

        # the rest 
        # look into default=argparse.SUPPRESS and k,v these into self.dict
        if ns.instance_type:
            self.instance_type = ns.instance_type
        if ns.ami:
            self.ami= ns.ami
        if ns.vpc_id:
            self.vpc_id= ns.vpc_id
        if ns.subnet_id:
            self.subnet_id= ns.subnet_id
        if ns.key_name:
            self.key_name= ns.key_name



