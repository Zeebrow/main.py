import pytest
import argparse

import quickhost

should_pass = [ "aws -n asdf --port 22 --port 22 --ip 1.2.3.4/24 ".split(), ]


#@pytest.fixture
#def cli_line(app_name: str, config_file=None):
#    _line = "aws"
#    if config_file is not None:
#        _line = "--config-file " _config_file + " " + _line
#    _line = _line + " -n " + app_name
#    return _line

@pytest.fixture
def new_parser():
    def _new_app_parser():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS)
        quickhost.AWSApp.parser_arguments(subparser=subparsers)
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
