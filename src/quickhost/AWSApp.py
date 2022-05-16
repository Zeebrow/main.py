from typing import List
from dataclasses import dataclass
from argparse import Namespace, SUPPRESS, ArgumentParser, _ArgumentGroup
from abc import ABCMeta, abstractmethod
import configparser
import logging
from os import get_terminal_size
import json

import boto3

from .utilities import get_my_public_ip
from .constants import *
from .cli_params import AppBase, AppConfigFileParser
from .SG import SG
from .AWSHost import AWSHost

logger = logging.getLogger(__name__)

AWS_DESCRIBE = 0
AWS_MAKE = 1
AWS_UPDATE = 2
AWS_DESTROY = 3

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
        self.sgid = None
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
    def parser_arguments(self, subparser: ArgumentParser) -> None:
        # 'really good' argparse example at community vmware https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/tools/cli.py
        def qh_add_make_update(mu_arg_group: ArgumentParser) -> None:
            mu_arg_group.add_argument("-n", "--app-name", required=True, help="Name the group of hosts you're creating (remember, there is no state!)")
            mu_arg_group.add_argument("-y", "--dry-run", required=False, action='store_true', help="prevents any resource creation when set")
            mu_arg_group.add_argument("-c", "--host-count", required=False, default=1, help="number of hosts to create")
            mu_arg_group.add_argument("-p", "--port", required=False, type=int, action='append', default=SUPPRESS, help="add an open tcp port to security group, applied to all ips")
            mu_arg_group.add_argument("--ip", required=False, action='append', help="additional ipv4 to allow through security group. all ports specified with '--port' are applied to all ips specified with --ip if a cidr is not included, it is assumed to be /32")
            mu_arg_group.add_argument("--instance-type", required=False, default="t2.micro", help="change the type of instance to launch")
            mu_arg_group.add_argument("--ami", required=False, default=SUPPRESS, help="change the ami to launch, see source-aliases for getting lastest")
            mu_arg_group.add_argument("-u", "--userdata", required=False, default=SUPPRESS, help="path to optional userdata file")
            mu_arg_group.add_argument("--vpc-id", required=False, default=SUPPRESS, help="specify a VpcId to choose the vpc in which to launch hosts")
            mu_arg_group.add_argument("--subnet-id", required=False, default=SUPPRESS, help="specify a SubnetId to choose the subnet in which to launch hosts")
            mu_arg_group.add_argument("--key-name", required=False, default=SUPPRESS, help="specify the name of an EC2 keypair to use for accessing hosts")

        def qh_add_describe_destroy(arg_group: ArgumentParser) -> None:
            arg_group.add_argument("-n", "--app-name", required=True, help="Name the group of hosts you're creating (remember, there is no state!)")


        qh_main = subparser.add_subparsers()
        qhmake = qh_main.add_parser("make")
        qhdescribe = qh_main.add_parser("describe")
        qhupdate = qh_main.add_parser("update")
        qhdestroy = qh_main.add_parser("destroy")
        ### need to make a custom arg for each parser, so we can tell the difference after parser.parse_args() is called.
        # jankiness spotted?
        qhmake.set_defaults(__qhaction="make")
        qhdescribe.set_defaults(__qhaction="describe")
        qhupdate.set_defaults(__qhaction="update")
        qhdestroy.set_defaults(__qhaction="destroy")
        ###

        qh_add_make_update(qhmake)
        qh_add_describe_destroy(qhdescribe)
        qh_add_make_update(qhupdate)
        qh_add_describe_destroy(qhdestroy)

    def load_cli_args(self, args: dict):
        """eats what parser_arguments() sets up, overriding load_default_config() values"""
        self._client = boto3.client("ec2")

        # CRUD always available, @@@todo test
        if args['__qhaction'] == 'make':
            print('make')
            self.create(args)
            exit(0)
        elif args['__qhaction'] == 'describe':
            print('describe')
            self.describe(args)
            exit(0)
        elif args['__qhaction'] == 'update':
            print('update')
            print("@@@ not implemented")
            exit(0)
        elif args['__qhaction'] == 'destroy':
            print('destroy')
            print("@@@ not implemented")
            exit(0)
        else:
            raise Exception("should have printed help in main.py! Bug!")
    
    def _parse_make(self, args: dict):
        flags = args.keys()
        # ports ingress
        if 'port' in flags:
            # get rid of duplicates
            _ports = list(dict.fromkeys(args['port']))
            ports = []
            for p in _ports:
                # pretend they're all inst for now
                try:
                    ports.append(str(p))
                except ValueError:
                    raise RuntimeError("port numbers must be digits")
            self.ports = ports
        else:
            self.ports = [*DEFAULT_SG_PORTS]

        # cidrs ingress
        if args['ip'] is None:
            self.cidrs = [get_my_public_ip()]
        else:
            for i in args['ip']:
                if len(i.split('/')) == 1:
                    logger.warning(f"Assuming /32 cidr for ip '{i}'")
                    self.cidrs.append(i + "/32")
                else:
                    self.cidrs.append(i)

        # userdata
        if 'user_data' in flags:
            if not Path(args['userdata']).exists():
                raise RuntimeError(f"path to userdata '{args['userdata']}' does not exist!")
            self.userdata = flags['userdata']

        # the rest 
        # look into default=argparse.SUPPRESS and k,v these into self.dict
        if 'dry_run' in flags:
            self.dry_run = not args['dry_run']
        if 'host_count' in flags:
            self.num_hosts = args['host_count']
        if 'instance_type' in flags:
            self.instance_type = args['instance_type']
        if 'ami' in flags:
            self.ami= args['ami']
        if 'vpc_id' in flags:
            self.vpc_id= args['vpc_id']
        if 'subnet_id' in flags:
            self.subnet_id= args['subnet_id']
        if 'key_name' in flags:
            self.key_name= args['key_name']

    def _parse_describe(self, args: dict):
        """would feel empty without this function"""
        flags = args.keys()
        return
        
    def _parse_destroy(self, args: dict):
        flags = args.keys()
        if 'dry_run' in flags:
            self.dry_run = not ns.dry_run #NOT
        self._client = boto3.client("ec2")

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

    def describe(self, args: dict) -> None:
        self._parse_describe(args)
        _sg = SG(
            client=self._client,
            app_name=self.app_name,
            vpc_id=self.vpc_id,
            ports=self.ports,
            cidrs=self.cidrs,
            dry_run=self.dry_run,
        )
        self.print_loaded_args()
        print(_sg.get_security_group())

    def create(self, args: dict):
        self._parse_make(args)
        _sg = SG(
            client=self._client,
            app_name=self.app_name,
            vpc_id=self.vpc_id,
            ports=self.ports,
            cidrs=self.cidrs,
            dry_run=self.dry_run,
        )
        self.sgid = _sg.create()
        print("self ami ===>" + str(self.ami))
        if self.ami is None:
            print("No ami specified, getting latest al2...", end='')
            self.ami = AWSHost.get_latest_image(client=self._client)
            print(f"done ({self.ami})")
        _host = AWSHost(
            client=self._client,
            app_name=self.app_name,
            num_hosts=self.num_hosts,
            image_id=self.ami,
            instance_type=self.instance_type,
            subnet_id=self.subnet_id,
            sgid=self.sgid,
            key_name=self.key_name,
            userdata=self.userdata,
            dry_run=self.dry_run
        )
        _host.new_instances()

    def destroy(self):
        pass

