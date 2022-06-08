import json
import argparse
import sys
from os import get_terminal_size
import logging
import configparser
from pathlib import Path
from importlib import metadata
# TODO: move AppBase back, and have plugins import quickhost


DEFAULT_CONFIG_FILEPATH = str(Path("/opt/etc/quickhost/quickhost.conf").absolute())

logger = logging.getLogger()

fmt='%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s'
logger.setLevel(logging.WARNING)
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
        logger.error(f"No suitable plugin found for '{tgt_module}'. You might install it by running `pip install quickhost-{tgt_module}`.")
        exit(1)
    for plugin in available_plugins:
        if plugin.name == f"quickhost_{tgt_module}":
            return plugin.load()
#            plugin = ep.load()
#            app = plugin()

def app_parser_pass_1():
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

def app_parser_pass_2():
    app_parser = app_parser_pass_1()
    if len(sys.argv) == 1:
        print('helo')
        exit(1)

    app_args = vars(app_parser.parse_args())
    config_parser = AppConfigFileParser()
    _cfg_file = DEFAULT_CONFIG_FILEPATH 
    if 'config_file' in app_args.keys():
        _cfg_file = app_args['config_file']
    config_parser.read(_cfg_file)

    if app_args['__qhaction'] == 'init':
        app = load_plugin(app_args['app_name'])()(app_args['app_name'], config_file=_cfg_file)
        return app, app_parser

    # step 2 - infer 'aws' 
    for a in config_parser.sections():
        if ':' not in a:
            # not my yob
            continue
        tgt_app_name,tgt_plugin = a.split(':')
        if tgt_app_name == app_args['app_name']:
            app_config = config_parser[f"{app_args['app_name']}:{tgt_plugin}"]
            # step 3 load plugin
            app = load_plugin(tgt_plugin)()(app_args['app_name'], config_file=_cfg_file)
            return app, app_parser

    if app_args['__qhaction'] == 'make':
        app.make_parser_arguments(app_parser)
    return app, app_parser

app, parser = app_parser_pass_2()
args = vars(parser.parse_args())
print(args)
app.run(args)

exit()

