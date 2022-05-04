import pytest
from pathlib import Path
from argparse import ArgumentParser, Namespace, SUPPRESS
import logging

from quickhost import AWSConfig
from fixtures.fixt_aws_cli import new_parser

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

def test_load_config_cli_arg(new_parser):
    cfg_file = 'tests/data/another_test_aws_config.conf'
    cfg2 = Path('tests/data/another_test_aws_config.conf')
    app_name = 'test_load_config_cli_arg'

    cli_args = " --config-file " + cfg_file
    cli_args += " aws"
    cli_args += " -n test_load_config_cli_arg \
            --port 30 \
            --port 22 \
            --port 22 \
            --ip 1.2.3.4/24 \
            --ip 3.2.1.5 \
            --vpc-id vpc-overrides \
            --subnet-id subnet-cli-override"
    cli_args = cli_args.split()

    parser = new_parser()
    args = parser.parse_args(cli_args)
    c = AWSConfig(app_name=args.app_name, config_file=args.config_file)

    assert c.subnet_id == 'subnet-asdf9876'
    assert c.vpc_id == 'vpc-asdf9876'
    c.load_cli_args(args)
    assert c.app_name == app_name
    assert c.config_file == cfg2.absolute()
    assert '1.2.3.4/24' in c.cidrs
    assert '3.2.1.5/32' in c.cidrs
    for p in c.ports:
        assert type(p) == type(int())
    assert len(c.ports) == 2
    assert c.subnet_id == 'subnet-cli-override'
    assert c.vpc_id == 'vpc-overrides'


def test_load_aws_config_cli_overrides_file():
    should_pass = [
        "aws -n asdf --port 22 --port 22 --ip 1.2.3.4/24 ".split(),
    ]
    # @@@ fixture, or what?
    for sp in should_pass:
        parser = ArgumentParser('test_load')
        subparsers = parser.add_subparsers()
        parser.add_argument("-f", "--config-file", required=False, default=SUPPRESS)
        
        AWSConfig.parser_arguments(subparser=subparsers)
        args = parser.parse_args(sp)

        _a = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': cfg_file} if not 'config_file' in vars(args).keys() else {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': args.config_file}

        c = AWSConfig(**_a)
        print(c.__dict__)
        assert c.subnet_id == 'subnet-9876'
        assert c.vpc_id == 'vpc-9876'
        c.load_cli_args(args)
        assert len(c.ports) == 1


