#!/usr/bin/env python3
import json
import argparse
import sys
from os import get_terminal_size
import logging

from quickhost import AWSApp

logger = logging.getLogger()

fmt='%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s'
logger.setLevel(logging.WARNING)
sh = logging.StreamHandler()
logger.addHandler(sh)

parser = argparse.ArgumentParser(description="make a bunch of ec2 servers, relatively quickly")
parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS, help="Use an alternative to quickhost.conf for default configuration")
parser.add_argument("--print-config", required=False, action='store_true', help="Print the config params to be used")

subparsers = parser.add_subparsers()
aws_subparser = subparsers.add_parser('aws')
AWSApp.parser_arguments(subparser=aws_subparser)

args = vars(parser.parse_args())

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

if not '__qhaction' in args.keys():
    aws_subparser.print_help()
    exit()
if not 'config_file' in args.keys():
    _a = {'app_name': args['app_name']}
else:
    _a = {'app_name': args['app_name'], 'config_file': args['config_file']}
    
aws = AWSApp(**_a)
aws.load_cli_args(args)

if args.print_config:
    print(f"{args.print_config=}")
    aws._print_loaded_args("your config:")
    exit(1)
