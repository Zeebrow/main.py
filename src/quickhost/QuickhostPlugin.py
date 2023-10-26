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

import logging
import sys

if sys.version_info.minor == 7:
    import pkgutil
else:
    from importlib import metadata

import typing as t

from collections import defaultdict
from dataclasses import dataclass

from .quickhost_app_base import AppBase, ParserBase

logger = logging.getLogger(__name__)

PluginName = str

@dataclass
class Plugin:
    """
    Container object for plugin-loading functions
    """
    name: PluginName
    package_name: str
    version: str
    app: AppBase
    parser: ParserBase


class QHPlugin:
    @classmethod
    def load_all_plugins(cls) -> t.Dict[PluginName, Plugin]:
        """returns a dictionary mapping installed plugin names to a Plugin object"""
        plugins = defaultdict(dict)

        if sys.version_info.minor == 7:
            for p in pkgutil.walk_packages():
                if p.name.startswith('quickhost_') and p.ispkg:
                    l = pkgutil.get_loader(p.name).load_module()  # noqa: E741
                    # found in plugin's __init__.py
                    provider_name = p.name.split('_')[1]
                    package_name = 'quickhost_' + provider_name
                    version = "undefined"
                    app = l.load_plugin()
                    parser = l.get_parser()
                    plugins[provider_name] = Plugin(name=provider_name, package_name=package_name, version=version, app=app, parser=parser)

            return dict(plugins)

        elif sys.version_info.minor > 7 and sys.version_info.minor < 10:
            plugin_parsers = metadata.entry_points()['quickhost_plugin']
        else:
            plugin_parsers = metadata.entry_points().select(group="quickhost_plugin")


        # sift through plugins, organize by cloud provider and return
        for p in plugin_parsers:
            provider_name = p.name.split('_')[0]
            package_name = 'quickhost_' + provider_name
            version = metadata.version("quickhost_{}".format(provider_name))
            # 'app' or 'parser'
            plugin_type = p.name.split('_')[1]
            if plugin_type == 'app':
                plugins[provider_name]['app'] = p.load()()
            elif plugin_type == 'parser':
                plugins[provider_name]['parser'] = p.load()()
            else:
                logger.warning(f"Unknown plugin type '{plugin_type}'")
        plugins_list: t.Dict[str, Plugin] = {
                p: Plugin(name=p, package_name=package_name, version=version, app=plugins[p]['app'], parser=plugins[p]['parser']) for p in plugins.keys()  # noqa: E126
        }
        return dict(plugins_list)
