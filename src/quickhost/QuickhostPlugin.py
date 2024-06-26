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
    import importlib_metadata as metadata
    from importlib_metadata import version
else:
    from importlib import metadata
    from importlib.metadata import version

import typing as t

from dataclasses import dataclass

from .quickhost_app_base import AppBase, ParserBase

logger = logging.getLogger(__name__)


PluginName = str


class NoPluginFoundError(Exception):
    pass


@dataclass
class Plugin:
    name: PluginName
    package_name: str
    version: str
    app: AppBase
    parser: ParserBase


def get_plugin(plugin_name: PluginName) -> Plugin:
    """
    Get a quickhost plugin that adheres to entrypoint naming conventions:

    :raises NoPluginFoundError: The pip package 'quickhost-<plugin_name>' is not installed
    :return: Plugin containing AppBase, Parser, and metadata
    :rtype: quickhost.QuickhostPlugin.Plugin

    [options.entry_points]
    quickhost_plugin =
        <plugin_name>_app = quickhost_<plugin_name>:get_app
        <plugin_name>_parser = quickhost_<plugin_name>:get_parser
    """

    qh_plugins = metadata.entry_points(group='quickhost_plugin')
    try:
        v = version(f'quickhost_{plugin_name}')
        app = qh_plugins[f'{plugin_name}_app'].load()()
        parser = qh_plugins[f'{plugin_name}_parser'].load()()
    except Exception as e:
        print(e)
        print(e)
        print(e)
        print(e)
        raise NoPluginFoundError(f"No plugin found for '{plugin_name}' -- try running pip install quickhost-{plugin_name}")

    return Plugin(
        name=plugin_name,
        package_name=f'quickhost_{plugin_name}',
        version=v,
        app=app,
        parser=parser,
    )


def get_plugin_app_getter(plugin_name: PluginName) -> t.Callable[..., AppBase]:
    """
    Get the loader a :class:`quickhost.quickhost_app_base.AppBase` subclass.

    :param name: Name of the plugin
    :type name: str
    :raises NoPluginFoundError: The pip package 'quickhost-<plugin_name>' is not installed
    :return: function returning the plugin's app class
    :rtype: quickhost.QuickhostPlugin.Plugin
    """
    try:
        qh_plugins = metadata.entry_points(group='quickhost_plugin')[f'{plugin_name}_app']
        return qh_plugins.load()
    # "do not use bare except" ???
    except:  # noqa: E722
        raise NoPluginFoundError(f"No plugin found for '{plugin_name}' -- try running pip install quickhost-{plugin_name}")


def get_plugin_parser_getter(plugin_name: PluginName) -> t.Callable[..., ParserBase]:
    """
    Get the loader a :class:`quickhost.quickhost_app_base.ParserBase` subclass.

    :param name: Name of the plugin
    :type name: str
    :raises NoPluginFoundError: The pip package 'quickhost-<plugin_name>' is not installed
    :return: function returning the plugin's parser class
    :rtype: Callable[..., ParserBase]
    """
    try:
        qh_plugins = metadata.entry_points(group='quickhost_plugin')[f'{plugin_name}_parser']
        return qh_plugins.load()
    except:  # noqa: E722
        raise NoPluginFoundError(f"No plugin found for '{plugin_name}' -- try running pip install quickhost-{plugin_name}")


def fetch_all_plugins() -> t.Dict[PluginName, Plugin]:
    """
    Eagerly loads all quickhost plugins.
    Returns a dictionary mapping installed plugin names to a Plugin object

    :return: dict mapping plugin names to their :class:`quickhost.QuickhostPlugin.Plugin`.
    :rtype: Dict[str, Plugin]
    """
    plugins = {}
    plugin_providers = set([entrypoint.name.split('_')[0] for entrypoint in metadata.entry_points(group='quickhost_plugin')])
    logger.debug("Found %d provider plugins.", len(plugin_providers))
    for p in plugin_providers:
        plugins[p] = get_plugin(p)
    return plugins
