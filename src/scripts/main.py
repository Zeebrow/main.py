import json
import argparse
import sys
from os import get_terminal_size
import logging
import configparser
from pathlib import Path
from importlib import metadata
# TODO: move AppBase back, and have plugins import quickhost


DEFAULT_CONFIG_FILEPATH = str(Path().home() / ".local/etc/quickhost.conf")

logger = logging.getLogger()

fmt='%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s'
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
logger.addHandler(sh)

class AppConfigFileParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__(allow_no_value=True)

def load_plugin(tgt_module: str):
    """step 3 load plugin, Somehow™ """
    try:
        available_plugins = metadata.entry_points()['quickhost_plugin']
    except KeyError:
        logger.error(f"No quickhost plugins are installed")
    for plugin in available_plugins:
        logger.debug(f"+++> {plugin}")
        logger.debug(f"+++> {plugin.name}")
        if plugin.name == f"quickhost_{tgt_module}":
            app = plugin.load()()
            logger.debug(plugin._asdict())
            logger.debug(type(app))
            #return plugin.load()
            return app
#            plugin = ep.load()
#            app = plugin()

def get_main_parser():
    parser = argparse.ArgumentParser(description="make easily managed hosts, quickly")
    # aah im gonna hate this
    parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS, help="Use an alternative configuration file to override the default.")
    qh_main = parser.add_subparsers()
    qhinit      = qh_main.add_parser("init").set_defaults(__qhaction="init")
    qhmake      = qh_main.add_parser("make").set_defaults(__qhaction="make")
    qhdescribe  = qh_main.add_parser("describe").set_defaults(__qhaction="describe")
    qhupdate    = qh_main.add_parser("update").set_defaults(__qhaction="update")
    qhdestroy   = qh_main.add_parser("destroy").set_defaults(__qhaction="destroy")
    parser.add_argument("app_name", default=argparse.SUPPRESS, help="app name")
    return parser

def get_app():
    app_parser = get_main_parser()
    if len(sys.argv) == 1:
        app_parser.print_help()
        exit(1)
    app_args = vars(app_parser.parse_args())
    print(f"{app_args=}")
    if not 'app_name' in app_args.keys():
        app_parser.print_usage()
        exit(1)

    config_parser = AppConfigFileParser()
    _cfg_file = DEFAULT_CONFIG_FILEPATH 
    if 'config_file' in app_args.keys():
        _cfg_file = app_args['config_file']
    config_parser.read(_cfg_file)

    tgt_plugin_name = None
    for sec in config_parser.sections():
        if app_args['app_name'] in sec:
            tgt_plugin_name = sec.split(":")[1]
            break
    app_config = config_parser[f"{app_args['app_name']}:{tgt_plugin_name}"]
    app = load_plugin(tgt_plugin_name)(app_args['app_name'], config_file=_cfg_file)

    action = app_args['__qhaction']
    if action == 'init':
        #app = load_plugin(tgt_plugin_name)(app_args['app_name'], config_file=_cfg_file)
        return app, app_parser
    elif action == 'make':
        app.make_parser_arguments(app_parser)
        return app, app_parser
    else:
        logger.error(f"No such action '{action}'")
        exit(1)
    return None, None

app, parser = get_app()
args = vars(parser.parse_args())
print(args)
app.run(args=args)

exit()

