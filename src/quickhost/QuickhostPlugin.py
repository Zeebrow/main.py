import logging
from importlib import metadata
from .quickhost_app_base import AppBase
from .constants import QHExit

logger = logging.getLogger(__name__)

class QHPlugin:

    @classmethod
    def load_all_plugins(self):
    #def load_all_plugins(self, init_parser):
        available_plugins = {}
        plugins = metadata.entry_points().select(group="quickhost_plugin")
        for p in plugins:
            #_app = p.load()(init_parser)
            _app = p.load()()
            available_plugins[_app.plugin_name] = _app
        return available_plugins 

    @classmethod
    def load_plugin(self, tgt_module: str):
        plugin = metadata.entry_points().select(name=f"quickhost_{tgt_module}")
        if list(plugin) == []:
            logger.error(f"No such plugin 'quickhost_{tgt_module}' is installed.")
            exit(QHExit.GENERAL_FAILURE)
        logger.debug(f"Found plugin '{plugin}'")
        app_class = tuple(plugin)[0].load()
        return app_class

    def get_app(self) -> AppBase:
        pass

