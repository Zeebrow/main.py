import pytest
from pathlib import Path
from argparse import ArgumentParser, Namespace, SUPPRESS
import logging

from quickhost import AWSConfig

cfg_file = Path('tests/data/test_aws_config.conf').absolute()

def test_load_fnf_raises():
    with pytest.raises(RuntimeError):
        c = AWSConfig('test_load_aws_config_file', 'gobbldiegook')

def test_load_aws_config_file():
    c = AWSConfig('test_load_aws_config_file', cfg_file)
    assert c.subnet_id == 'subnet-abc123'
    assert c.vpc_id == 'vpc-_all'

def test_app_config_overrides__all():
    c = AWSConfig('test_app_config_overrides__all', cfg_file)
    assert c.subnet_id != 'subnet-_all'
    assert c.vpc_id != 'vpc-_all'

def test_load_aws_config_cli_overrides_file():
    should_pass = [
        "-n asdf aws --port 22 --port 22 --ip 1.2.3.4/24 ".split(),
    ]
    for sp in should_pass:

        parser = ArgumentParser('test_load')
        subparsers = parser.add_subparsers()
        parser.add_argument("-n", "--app-name", required=True)
        parser.add_argument("-f", "--config-file", required=False, default=SUPPRESS)
        
        AWSConfig.parser_arguments(subparser=subparsers)
        args = parser.parse_args(sp)

        _a = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': cfg_file} if not 'config_file' in vars(args).keys() else {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': args.config_file}

        print(f"{args=}")
        #c = AWSConfig('test_load_aws_config_file', cfg_file)
        c = AWSConfig(**_a)
        print(c.__dict__)
        assert c.subnet_id == 'subnet-9876'
        assert c.vpc_id == 'vpc-9876'
        c.load_cli_args(args)
        assert len(c.ports) == 1


