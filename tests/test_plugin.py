# Copyright (C) 2022 zeebrow

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import pytest

from quickhost import QHPlugin, AppBase

import argparse


def test_null_plugin_loads():
    plugins = QHPlugin.load_all_plugins()
    assert 'null' in plugins.keys()


def test_load_plugin_returns_app_class():
    plugins = QHPlugin.load_all_plugins()
    null_app_class = plugins['null']['app']()
    assert type(null_app_class) == type(AppBase)
    # @@@
    # null_app_instance = null_app_class(app_name="some-app")
    # assert type(null_app_class) == type(NullApp)


def test_load_plugin_parser():
    plugins = QHPlugin.load_all_plugins()
    null_app_parser = plugins['null']['parser']()()
    print(type(null_app_parser))


@pytest.mark.skip
def test_plugin_parser_provides_app_name_arg(self):
    for action in ['make', 'describe', 'update', 'destroy']:
        parser = argparse.ArgumentParser(self._testMethodName)
        plugins = QHPlugin.load_all_plugins()
        null_parser = plugins['null']['parser']()()
        null_parser.add_parser_arguments(action, parser)
        args = parser.parse_args(['--app-name', 'test_app_name'])
        self.assertIsNotNone(args.app_name)
