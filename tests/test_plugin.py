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

from quickhost import QHPlugin, AppBase
import unittest
import argparse


class TestLoadPlugin(unittest.TestCase):
    
    def test_null_plugin_loads(self):
        plugins = QHPlugin.load_all_plugins()
        # print(plugins)
        assert 'null' in plugins.keys()

    def test_load_plugin_returns_app_class(self):
        plugins = QHPlugin.load_all_plugins()
        null_app_class = plugins['null']['app']()
        assert type(null_app_class) == type(AppBase)
        null_app = null_app_class()
        # print(type(null_app)) # <class 'quickhost_null.NullApp.NullApp'>
        # this is a frivolous test...
        self.assertNotEqual(type(null_app_class), type(null_app))

        #@@@ want a better way to show that we have an instance of the class, without doing any config loading etc.
        # e.g. plugin_version(), display_license(), metadata, ...
        self.assertIsNotNone(null_app.about())


class TestPluginCLIConventions(unittest.TestCase):

    def test_plugin_parser_provides_app_name_arg(self):
        """
        :thinking_emoji: is this a 'good' test? It really just exposes a desgin flaw of requiring an 'app name'
        to be provided by the user. What if that changes in the future? :/thinking_emoji:
        """
        for action in ['make', 'describe', 'update', 'destroy']:
            #@@@ need a new parser for each test - is there a 'pythonic' way to do this?
            parser = argparse.ArgumentParser(self._testMethodName)
            plugins = QHPlugin.load_all_plugins()
            null_parser = plugins['null']['parser']()()
            null_parser.add_parser_arguments(action, parser)
            args = parser.parse_args(['--app-name', 'test_app_name'])
            self.assertIsNotNone(args.app_name)


    


if __name__ == '__main__':
    unittest.main()