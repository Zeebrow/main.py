from typing import List
from dataclasses import dataclass
from argparse import Namespace, SUPPRESS
from abc import ABCMeta, abstractmethod
import configparser
import logging
from os import get_terminal_size

import boto3

from .utilities import get_my_public_ip
from .constants import *
from .cli_params import AppBase, AppConfigFileParser
from .SG import SG

logger = logging.getLogger(__name__)

class AWSApp(AppBase):
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

        self._client = None

    def _all_cfg_key(self):
        return f'{self._cli_parser_id}:_all'

    def _app_cfg_key(self):
        return f'{self._cli_parser_id}:{self.app_name}'

    def load_default_config(self):
        """read values from config file, and import the relevant ones"""
        try:
            all_config = self._config_file_parser[self._all_cfg_key()]
            for k in all_config:
                if k in self.__dict__.keys():
                    self.__dict__[k] = self._config_file_parser[self._all_cfg_key()][k]
                else:
                    logger.warning(f"Ignoring bad param in config: '{k}'")
        except KeyError:
            logger.debug(f"No '_all' config ({self._all_cfg_key()}) found in config file '{self.config_file}'")
            all_config = None
        try:
            app_config = self._config_file_parser[self._app_cfg_key()]
            for k in app_config:
                if (k in self.__dict__.keys()) and (not k.startswith('_')):
                    self.__dict__[k] = self._config_file_parser[self._app_cfg_key()][k]
                else:
                    logger.warning(f"Ignoring bad param in config: '{k}'")
        except KeyError:
            logger.debug(f"No app config ({self._app_cfg_key()}) found in config file '{self.config_file}'")
            app_config = None

    @classmethod
    def parser_arguments(self, subparser: any) -> None:
        aws_subparser = subparser.add_parser('aws')

        aws_subparser.add_argument("--describe", required=False, default=SUPPRESS, action='store_true', help="Name the group of hosts you're creating (remember, there is no state!)")

        aws_subparser.add_argument("-n", "--app-name", required=True, help="Name the group of hosts you're creating (remember, there is no state!)")
        aws_subparser.add_argument("-y", "--dry-run", required=False, action='store_true', help="prevents any resource creation when set")
        aws_subparser.add_argument("-c", "--host-count", required=False, default=1, help="number of hosts to create")
        aws_subparser.add_argument("-p", "--port", required=False, type=int, action='append', default=SUPPRESS, help="add an open tcp port to security group, applied to all ips")
        aws_subparser.add_argument("--ip", required=False, action='append', help="additional ipv4 to allow through security group. all ports specified with '--port' are applied to all ips specified with --ip if a cidr is not included, it is assumed to be /32")
        aws_subparser.add_argument("--instance-type", required=False, default="t2.micro", help="change the type of instance to launch")
        aws_subparser.add_argument("--ami", required=False, default=SUPPRESS, help="change the ami to launch, see source-aliases for getting lastest")
        aws_subparser.add_argument("-u", "--userdata", required=False, default=SUPPRESS, help="path to optional userdata file")
        aws_subparser.add_argument("--vpc-id", required=False, default=SUPPRESS, help="specify a VpcId to choose the vpc in which to launch hosts")
        aws_subparser.add_argument("--subnet-id", required=False, default=SUPPRESS, help="specify a SubnetId to choose the subnet in which to launch hosts")
        aws_subparser.add_argument("--key-name", required=False, default=SUPPRESS, help="specify the name of an EC2 keypair to use for accessing hosts")


    def load_cli_args(self, ns: Namespace):
        """eats what parser_arguments() sets up, overriding load_default_config() values"""
        flags = vars(ns).keys()




        # ports ingress
        if 'port' in flags:
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
        if 'user_data' in flags:
            if not Path(ns.userdata).exists():
                raise RuntimeError(f"path to userdata '{ns.userdata}' does not exist!")
            self.userdata = ns.userdata

        # the rest 
        # look into default=argparse.SUPPRESS and k,v these into self.dict
        if 'dry_run' in flags:
            self.dry_run = not ns.dry_run #NOT
        if 'host_count' in flags:
            self.num_hosts = ns.host_count
        if 'instance_type' in flags:
            self.instance_type = ns.instance_type
        if 'ami' in flags:
            self.ami= ns.ami
        if 'vpc_id' in flags:
            self.vpc_id= ns.vpc_id
        if 'subnet_id' in flags:
            self.subnet_id= ns.subnet_id
        if 'key_name' in flags:
            self.key_name= ns.key_name


        ###
        # got all the info we need, make client
        self._client = boto3.client("ec2")


        if 'describe' in flags:
            self.print_loaded_args()
            self.describe()
            exit(0)


    def print_loaded_args(self) -> None:
        print()
        print(f"loaded config:")
        print(f"--------------")
        if get_terminal_size()[0] > 80:
            _w = 40
        else:
            _w = get_terminal_size()[0] 
        for k,v in self.__dict__.items():
            if not k.startswith("_"):
                print(k.ljust(_w,'.'), v)
        return None

    def describe(self) -> None:
        _sg = SG(
            client=self._client,
            app_name=self.app_name,
            vpc_id=self.vpc_id,
            ports=self.ports,
            cidrs=self.cidrs,
            dry_run=self.dry_run,
        )
        print(_sg.get_security_group())

    def create(self):
        _sg = SG(
            client=self._client,
            app_name=self.app_name,
            vpc_id=self.vpc_id,
            ports=self.ports,
            cidrs=self.cidrs,
            dry_run=self.dry_run,
        )
        _sg.create()
        _sg.add_ingress([80,443], ['0.0.0.0/0'])
        return _sg.sgid

    def destroy(self):
        pass

