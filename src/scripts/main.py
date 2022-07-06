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

from quickhost import AppBase, APP_CONST as C, QHExit, QHPlugin


#DEFAULT_CONFIG_FILEPATH = str(Path().home() / ".local/etc/quickhost.conf")

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

def load_all_plugins():
    #note this is to remove the need for app_name from the main parser. it shouldn't need to care.
    return metadata.entry_points().select(group="quickhost_plugin")

def _load_plugin(tgt_module: str):
    plugin = metadata.entry_points().select(name=f"quickhost_{tgt_module}")
    if len(list(plugin)) > 1:
        logger.error(f"Oops, this is a bug.\nIt appears you have two plugins named 'quickhost_{tgt_module}', perhaps try reinstalling them?")
        exit(QHExit.KNOWN_ISSUE)
    if list(plugin) == []:
        logger.error(f"No such plugin 'quickhost_{tgt_module}' is installed.")
        exit(QHExit.GENERAL_FAILURE)
    logger.debug(f"Found plugin '{plugin}'")
    app = tuple(plugin)[0].load()()
    return app

def load_plugin(tgt_module: str):
    plugin = metadata.entry_points().select(name=f"quickhost_{tgt_module}")
    if list(plugin) == []:
        logger.error(f"No such plugin 'quickhost_{tgt_module}' is installed.")
        exit(QHExit.GENERAL_FAILURE)
    logger.debug(f"Found plugin '{plugin}'")
    app_class = tuple(plugin)[0].load()
    return app_class

def get_app():
######################################################################################3
# main ArgumentParser
######################################################################################3
    app_parser = argparse.ArgumentParser(description="make easily managed hosts, quickly")
    #app_parser.add_argument("-f", "--config-file", required=False, default=argparse.SUPPRESS, help="Use an alternative configuration file to override the default.")
    app_parser.add_argument("-f", "--config-file", required=False, help="Use an alternative configuration file to override the default.")
    qh_main = app_parser.add_subparsers()
    qhinit      = qh_main.add_parser("init")
    qhinit.set_defaults(__qhaction="init")
    qhmake      = qh_main.add_parser("make")
    qhmake.set_defaults(__qhaction="make")
    qhdescribe  = qh_main.add_parser("describe")
    qhdescribe.set_defaults(__qhaction="describe")
    qhupdate    = qh_main.add_parser("update")
    qhupdate.set_defaults(__qhaction="update")
    qhdestroy   = qh_main.add_parser("destroy")
    qhdestroy.set_defaults(__qhaction="destroy")

    # place to store non-main cli args
    action_ns = argparse.Namespace()

######################################################################################3
# handle plugins
######################################################################################3
    # get a mapping of app_class from all available plugins 
    plugins = QHPlugin.load_all_plugins()
    logger.debug(f"loaded {len(plugins.keys())} plugins")

    # tell the parser about the plugin
    for plugin_name in plugins.keys():
        qhinit.add_argument(f"--{plugin_name}", action='store_true', dest=f"plugin_{plugin_name}")

    _args = app_parser.parse_known_args()
    cli_args = vars(_args[0])
    action_cli_args = _args[1]
    logger.debug(f"{cli_args=}")
    logger.debug(f"{action_cli_args=}")

    action = cli_args['__qhaction']
    config_file  = cli_args['config_file']
    
    #determine which plugin to use to create an instance of AppBase
    #the init action does not need any information other than the plugin
    tgt_plugin = None
    if action == 'init':
        # find the plugin that was specified on the cli
        for k,v in cli_args.items():
            if k.startswith('plugin_') and v == True:
                tgt_plugin = k.split('_')[1]
                break
        logger.debug(f"{tgt_plugin=}")
        load = QHPlugin.load_plugin(tgt_plugin)#(app_name, config_file=cfg_file)
        #app_class = load(app_parser)
        app_class = load()
        app = app_class
    else:
        app_config_parser = AppConfigFileParser()
        app_config_parser.read(C.DEFAULT_CONFIG_FILEPATH)
        apps = []
        #for s in app_config_parser.sections():





######################################################################################3
# parse action's arguments
######################################################################################3
    if action == 'init':
        app_name = tgt_plugin
        app = app_class(app_name, config_file)
        init_parser = app.get_init_parser()
        action_args = init_parser.parse_args(action_cli_args, namespace=action_ns)
        logger.debug(f"{action_args=}")
        app.run_init(vars(action_args))
        exit()
        return app, qhinit
    elif action == 'make':
        make_parser = app.get_make_parser()
        make_args = make_parser.parse_args(action_cli_args, namespace=action_ns)
        print(make_args)
        return
        #app.make_parser_arguments(app_parser)
        return app, app_parser
    elif action == 'describe':
        app.describe_parser_arguments(app_args)
        return app, app_parser
    elif action == 'destroy':
        return app, app_parser
    else:
        logger.error(f"No such action '{action}'")
        exit(QHExit.GENERAL_FAILURE)
    return None, None
    app = app_class(app)
    exit()

######################################################################################3
# old code?
######################################################################################3

    tgt_plugin_name = None
    #app_parser = get_main_parser()
    config_parser = AppConfigFileParser()
    cfg_file = C.DEFAULT_CONFIG_FILEPATH 
    if len(sys.argv) == 1:
        app_parser.print_help()
        exit(QHExit.GENERAL_FAILURE)
    #app_args = vars(app_parser.parse_args())
    app_args = vars(app_parser.parse_known_args()[0])
    app_name = app_args['app_name']
    action = app_args['__qhaction']
    if 'config_file' in app_args.keys():
        cfg_file = app_args['config_file']
    config_parser.read(cfg_file)

#    if not 'app_name' in app_args.keys():
#        app_parser.print_usage()
#        exit(QHExit.GENERAL_FAILURE)
#
#    if action != 'init':
#        for sec in config_parser.sections():
#            if app_name in sec:
#                tgt_plugin_name = sec.split(":")[1]
#                break
#        app = load_plugin(tgt_plugin_name)(app_name, config_file=cfg_file)
#    else:
#        app = load_plugin(app_name)(app_name, config_file=cfg_file)

    if action == 'init':
        #app.init_parser_arguments(app_parser)
        app.init_parser_arguments(qhinit)
        return app, qhinit
    elif action == 'make':
        app.make_parser_arguments(app_parser)
        return app, app_parser
    elif action == 'describe':
        app.describe_parser_arguments(app_args)
        return app, app_parser
    elif action == 'destroy':
        return app, app_parser
    else:
        logger.error(f"No such action '{action}'")
        exit(QHExit.GENERAL_FAILURE)
    return None, None

def main():
    exit_code = 0
    app, parser = get_app()
    args = vars(parser.parse_args())
    print(f"args before calling app.run: {args}")
    app.run(args=args)
    return exit_code

# HNG
exit(main())
