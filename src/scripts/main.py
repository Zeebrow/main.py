import json
import argparse
import sys
from os import get_terminal_size
import logging
import configparser
from pathlib import Path
from importlib import metadata
import warnings
# TODO: move AppBase back, and have plugins import quickhost

from quickhost import AppBase


DEFAULT_CONFIG_FILEPATH = str(Path().home() / ".local/etc/quickhost.conf")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
debug_fmt='%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s'
fmt='%(levelname)s: %(message)s'
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter(debug_fmt))
logger.addHandler(sh)

class AppConfigFileParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__(allow_no_value=True)

def load_plugin(tgt_module: str):
    """step 3 load plugin, Somehow™ """
    plugin = metadata.entry_points().select(name=f"quickhost_{tgt_module}")
    if len(list(plugin)) > 1:
        logger.error(f"Oops, this is a bug.\nIt appears you have two plugins named 'quickhost_{tgt_module}', perhaps try reinstalling them?")
        sys.exit(1)
    if list(plugin) == []:
        logger.error(f"No such plugin 'quickhost_{tgt_module}' is installed.")
        sys.exit(1)
    logger.debug(f"Found plugin '{plugin}'")
    app = tuple(plugin)[0].load()()
    return app

def get_main_parser():
    parser = argparse.ArgumentParser(description="make easily managed hosts, quickly")
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
    tgt_plugin_name = None
    app_parser = get_main_parser()
    config_parser = AppConfigFileParser()
    cfg_file = DEFAULT_CONFIG_FILEPATH 
    if len(sys.argv) == 1:
        app_parser.print_help()
        exit(1)
    app_args = vars(app_parser.parse_args())
    app_name = app_args['app_name']
    action = app_args['__qhaction']
    if 'config_file' in app_args.keys():
        cfg_file = app_args['config_file']
    config_parser.read(cfg_file)

    if not 'app_name' in app_args.keys():
        app_parser.print_usage()
        exit(1)

    if action == 'init':
        app = load_plugin(app_name)(app_name, config_file=cfg_file)
        app.init_parser_arguments(app_parser)
        args = vars(app_parser.parse_args())
        app.plugin_init(args)
        exit(0)

    for sec in config_parser.sections():
        if app_name in sec:
            tgt_plugin_name = sec.split(":")[1]
            break
    app_config = config_parser[f"{app_name}:{tgt_plugin_name}"]
    app = load_plugin(tgt_plugin_name)(app_name, config_file=cfg_file)

    if action == 'make':
        app.make_parser_arguments(app_parser)
        return app, app_parser
    elif action == 'describe':
        app.describe(app_parser)
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

