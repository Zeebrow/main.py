import unittest
import pytest
from pathlib import Path
from argparse import ArgumentParser, Namespace, SUPPRESS
import logging

from quickhost import AWSApp
from fixtures.fixt_aws_cli import new_parser


cfg_file = Path('tests/data/test_aws_config.conf').absolute()

class TestConfig(unittest.TestCase):

    def test_load_filenotfound_raises(self):
        with pytest.raises(RuntimeError):
            c = AWSApp('test_load_aws_config_file', 'gobbldiegook')

    def test_load_aws_config_file(self):
        c = AWSApp(app_name='test_load_aws_config_file', config_file=cfg_file)
        assert c.subnet_id == 'subnet-abc123'
        assert c.vpc_id == 'vpc-_all'

    def test_app_config_overrides__all(self):
        c = AWSApp(app_name='test_app_config_overrides__all', config_file=cfg_file)
        assert c.vpc_id == 'vpc-OVERRIDDEN'
        assert c.subnet_id == 'subnet-OVERRIDDEN'


