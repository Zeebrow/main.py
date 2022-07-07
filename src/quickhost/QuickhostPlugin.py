import logging
from importlib import metadata
import sys

from .quickhost_app_base import AppBase
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
        available_plugins = {}
        if sys.version_info.minor < 10:
            print(metadata.entry_points())
            plugins = metadata.entry_points()['quickhost_plugin']
        else:
            plugins = metadata.entry_points().select(group="quickhost_plugin")
        for p in plugins:
            _app = p.load()()
            available_plugins[_app.plugin_name] = _app
        return available_plugins 

    @classmethod
    def load_plugin(self, tgt_module: str):
        if sys.version_info.minor < 10:
            for p in metadata.entry_points()['quickhost_plugin']:
                if p[0].endswith(tgt_module):
                    app_class = p.load()
                    logger.debug(f"Found plugin '{plugin}'")
                    return app_class
            logger.error(f"No such plugin 'quickhost_{tgt_module}' is installed.")
            exit(QHExit.GENERAL_FAILURE)
        else:
            plugin = metadata.entry_points().select(name=f"quickhost_{tgt_module}")
        if list(plugin) == []:
            logger.error(f"No such plugin 'quickhost_{tgt_module}' is installed.")
            exit(QHExit.GENERAL_FAILURE)
        logger.debug(f"Found plugin '{plugin}'")
        app_class = tuple(plugin)[0].load()
        return app_class

    def get_app(self) -> AppBase:
        pass

