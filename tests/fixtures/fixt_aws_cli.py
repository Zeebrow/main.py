import pytest
import argparse

import quickhost


@pytest.fixture
def new_parser():
    def _new_app_parser():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS)
        aws_subparser = subparsers.add_parser('aws')
        quickhost.AWSApp.parser_arguments(subparser=aws_subparser)
        return parser
    return _new_app_parser


#    args = parser.parse_args(sp)
#
#        if not 'config_file' in vars(args).keys():
#            _a = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': cfg_file}
#        else:
#            _a = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': args.config_file}
#
#        c = AWSApp(**_a)
