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
from importlib import metadata
import sys
from collections import defaultdict

from .constants import QHExit

logger = logging.getLogger(__name__)


class QHPlugin:
    """
    for python < 3.10
    https://bugs.python.org/issue44246
    https://github.com/python/importlib_metadata/pull/278/files#
    """

    @classmethod
    def load_all_plugins(self):
        # plugins= {'aws': {'app': asdf[0].load(), 'parser': asdf[1].load()}}
        plugins = defaultdict(dict)

        if sys.version_info.minor < 10:
            plugin_parsers = metadata.entry_points()['quickhost_plugin']
        else:
            plugin_parsers = metadata.entry_points().select(group="quickhost_plugin")

        # sift through plugins, organize by cloud provider and return
        for p in plugin_parsers:
            provider_name = p.name.split('_')[0]
            plugin_type = p.name.split('_')[1]
            if plugin_type == 'app':
                plugins[provider_name]['app'] = p.load()
            elif plugin_type == 'parser':
                plugins[provider_name]['parser'] = p.load()
            else:
                logger.warning(f"Unknown plugin type '{plugin_type}'")
        # print(plugins)
        # print(dict(plugins))
        if dict(plugin_parsers) == {}:
            logger.error("No plugins are installed!")
            sys.exit(QHExit.GENERAL_FAILURE)
        return dict(plugins)
