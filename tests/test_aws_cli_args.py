import unittest
from unittest.mock import patch
import pytest
from pathlib import Path
import re

from quickhost import AWSApp

from fixtures.fixt_aws_cli import new_parser
from fixtures.sg_client_responses import patched_describe_sg, patched_describe_kp, patched_describe_host

cfg_file = Path('tests/data/test_aws_config.conf').absolute()

#@patch('boto3.client')
#class PatchedApp(AWSApp):
#    pass

def test_load_config_cli_arg(capsys):
    user_overridden_cfg_file = 'tests/data/another_test_aws_config.conf'
    app_name = 'test_load_config_cli_arg'
    pretend_arparser_args = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': user_overridden_cfg_file}

    c = AWSApp(**pretend_arparser_args)
    assert c.config_file == Path(user_overridden_cfg_file).absolute()
    pretend_aws_args = {
        "__qhaction": None,
        "app_name": "asdf",
        "port": [ "123", "80" ],
        "ip": [ "1.2.3.4/24" ],
    }
    with pytest.raises(Exception):
        c.load_cli_args(pretend_aws_args)




@patch('boto3.client')
def test_aws_describe(mock_boto_client, capsys):
    """
    Check stdout prints correct values.
    This test will fail when pytest is not invoked with capture=sys.
    """

    # ???????
    mock_boto_client.return_value = mock_boto_client
    # ok,
    mock_boto_client.describe_security_groups.return_value = patched_describe_sg
    mock_boto_client.describe_key_pairs.return_value = patched_describe_kp
    mock_boto_client.describe_instances.return_value = patched_describe_host


    user_overridden_cfg_file = 'tests/data/another_test_aws_config.conf'
    app_name = 'test_load_config_cli_arg'
    pretend_arparser_args = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': user_overridden_cfg_file}

    c = AWSApp(**pretend_arparser_args)
    pretend_aws_args = {
        "__qhaction": 'describe',
        "app_name": "asdf",
    }

    # sgid....................................sg-04bf04a4a22a9f07e
    # kpid....................................key-0b4a1597913d76bd6
    # ec2ids..................................['i-0f34a77c50806fff2']
    sg_pat = re.compile(r'sgid(?:\.)*(?P<sgid_val>.*)')
    kp_pat = re.compile(r'kpid(?:\.)*(?P<kpid_val>.*)')
    host_pat = re.compile(r'ec2ids(?:\.)*\[\'(?P<ec2ids_val>i-[0-9a-f]*)\'\]')

    c.run(pretend_aws_args)
    captured = capsys.readouterr()

    # note to self: https://docs.python.org/3/library/re.html#search-vs-match
    sg_match = sg_pat.search(captured.out)
    kp_match = kp_pat.search(captured.out)
    host_match = host_pat.search(captured.out)
    assert sg_match.groups()[0] == 'sg-04bf04a4a22a9f07e'
    assert kp_match.groups()[0] == 'key-0b4a1597913d76bd6'
    assert host_match.groups()[0] == 'i-0f34a77c50806fff2'

def test_load_cli_args():
    pretend_argparser_args = {'app_name':'test_load_aws_config_cli_overrides_file', 'config_file': cfg_file}
    pretend_aws_args = {
        "__qhaction": "describe",
        "app_name": "asdf",
        "port": [ "123", "80" ],
        "ip": [ "1.2.3.4/24" ],
    }
#    c = AWSApp(**pretend_argparser_args)
#    with pytest.raises(SystemExit):
#        c.load_cli_args(pretend_aws_args)
#        assert 'loaded config:' in capsys.out

