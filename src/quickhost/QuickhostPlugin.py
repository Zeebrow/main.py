import logging
from importlib import metadata
from .quickhost_app_base import AppBase

logger = logging.getLogger(__name__)

class QHPlugin:

    @classmethod
    def load_all_plugins(self):
        #note this is to remove the need for app_name from the main parser. it shouldn't need to care.
        return metadata.entry_points().select(group="quickhost_plugin")

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

