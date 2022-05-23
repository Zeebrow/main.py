import unittest
from unittest.mock import patch
from pathlib import Path
#import pytest
import json

import boto3

from quickhost import AWSApp, SG

from fixtures.fixt_aws_cli import new_parser
from fixtures.sg_client_responses import patched_describe_sg

cfg_file = Path('tests/data/test_aws_config.conf').absolute()
app_name = 'test_load_aws_config_cli_overrides_file'

@patch('boto3.client')
def test_describe(mock_boto_client):
    t_ports = [ "123", "80", 42 ]
    t_cidrs = [ "1.2.3.4/24" ]
    mock_boto_client.return_value = mock_boto_client
    mock_boto_client.describe_security_groups.return_value = patched_describe_sg
    sg = SG(
        client=boto3.client(),
        app_name=app_name,
        vpc_id='vpc-_all',
        ports=None,
        cidrs=None,
        dry_run=False,
    )
    # equal to running app with 'aws describe'
    sg.describe()
    assert sg.sgid == 'sg-04bf04a4a22a9f07e'
    assert sg.ports is not None
    assert "123/tcp" in sg.ports
    assert "80/tcp" in sg.ports
    assert "42/tcp" in sg.ports
    

