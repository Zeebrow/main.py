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
from quickhost import QHPlugin
from quickhost_null import NullApp, NullParser

PLUGIN_NAME = 'null'


def test_null_plugin_loads():
    plugins = QHPlugin.load_all_plugins()
    assert PLUGIN_NAME in plugins.keys()


def test_load_plugin_returns_app_class():
    plugins = QHPlugin.load_all_plugins()
    null_app_class = plugins[PLUGIN_NAME]['app']()
    null_app_instance = null_app_class('some-app')
    assert isinstance(null_app_instance, NullApp)


def test_load_plugin_returns_plugin_parser():
    plugins = QHPlugin.load_all_plugins()
    null_app_parser = plugins[PLUGIN_NAME]['parser']()()
    assert isinstance(null_app_parser, NullParser)
