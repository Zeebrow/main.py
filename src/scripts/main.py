#!/usr/bin/env python3
import json
import argparse
import sys

from quickhost import AWSConfig

def do_args():
    parser = argparse.ArgumentParser(description="make a bunch of ec2 servers, relatively quickly")
    subparsers = parser.add_subparsers()
    parser.add_argument("-n", "--app-name", required=True, help="Name the group of hosts you're creating (remember, there is no state!)")
    parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS, help="Use an alternative to quickhost.conf for default configuration")

    AWSConfig.parser_arguments(subparser=subparsers)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args


if __name__ == "__main__":
    args = do_args()
    print(args)
    if not 'config_file' in vars(args).keys():
        _a = {'app_name': args.app_name}
    else:
        _a = {'app_name': args.app_name, 'config_file': args.config_file}
        

    aws = AWSConfig(**_a)
    print(aws.__dict__)
    aws.load_cli_args(args)
    print(aws.__dict__)



