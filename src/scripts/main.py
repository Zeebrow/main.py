import json
import argparse
import sys
from os import get_terminal_size
import logging
import configparser
from pathlib import Path
import importlib

from importlib import metadata
###
alleps = metadata.entry_points()
for k,v in alleps.items():
    print(f"{k}: {v}")
    print()
eps = metadata.entry_points()['quickhost_plugin']
print('---------')
print(eps)
for ep in eps:
    print(ep)
    plugin = ep.load()
    app = plugin.get_app()
print('---------')
exit()
###

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
    print(f"=======> {tgt_module}")
    tgt_module_name = f"quickhost_{tgt_module}"
    m = importlib.import_module("quickhost_aws")
    print(sys.modules.keys())
    if f"quickhost_{tgt_module_name}" not in sys.modules.keys():
        raise ImportError(f"No such modules '{tgt_module_name}' - install it with 'pip install {tgt_module_name}'")
    else:
        m = importlib.import_module(tgt_module_name)
        return m.App
    raise ImportError(f"Could not load required plugin for '{tgt_module}'")


def app_parser_pass_1():
    parser = argparse.ArgumentParser(description="make easily managed hosts, quickly")
    # aah im gonna hate this
    parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS, help="Use an alternative configuration file to override the default.")
    qh_main = parser.add_subparsers()
    qhmake      = qh_main.add_parser("make").set_defaults(__qhaction="make")
    qhdescribe  = qh_main.add_parser("describe")
    qhupdate    = qh_main.add_parser("update")
    qhdestroy   = qh_main.add_parser("destroy")
    qhdescribe.set_defaults(__qhaction="describe")
    qhupdate.set_defaults(__qhaction="update")
    qhdestroy.set_defaults(__qhaction="destroy")
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
    # step 2 - infer 'aws' 
    for a in config_parser.sections():
        if ':' not in a:
            # not my yob
            continue
        tgt_app_name,tgt_plugin = a.split(':')
        if tgt_app_name == app_args['app_name']:
            app_config = config_parser[f"{app_args['app_name']}:{tgt_plugin}"]
            # step 3 load plugin
            app = load_plugin(tgt_plugin)(app_args['app_name'], config_file=_cfg_file)
            # ...
        # ...

    if app_args['__qhaction'] == 'make':
        app.make_parser_arguments(app_parser)
    # ...
    return app, app_parser

app, parser = app_parser_pass_2()
args = vars(parser.parse_args())
print(args)
app.run(args)

exit()

