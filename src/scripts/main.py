import json
import argparse
import sys
from os import get_terminal_size
import logging
import configparser
from pathlib import Path
from importlib import metadata
import warnings

from quickhost import AppBase, APP_CONST as C, QHExit, QHPlugin


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
debug_fmt='%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s'
normal_fmt='%(levelname)s: %(message)s'
just_text='%(message)s'
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter(debug_fmt))
#sh.setFormatter(logging.Formatter(just_text))
logger.addHandler(sh)

def main():
######################################################################################3
# handle plugins
######################################################################################3
    plugins = QHPlugin.load_all_plugins()
    logger.debug(f"loaded {len(plugins.keys())} plugins")

######################################################################################3
# main ArgumentParser
######################################################################################3
    app_parser = argparse.ArgumentParser(description="make easily managed hosts, quickly")
    app_parser.add_argument("-f", "--config-file", required=False, help="Use an alternative configuration file to override the default.")
    qh_main = app_parser.add_subparsers()
    qhinit = qh_main.add_parser("init")
    qhmake = qh_main.add_parser("make")
    qhdescribe = qh_main.add_parser("describe")
    qhupdate = qh_main.add_parser("update")
    qhdestroy = qh_main.add_parser("destroy")

    qhinit.set_defaults(__qhaction="init")
    qhmake.set_defaults(__qhaction="make")
    qhdescribe.set_defaults(__qhaction="describe")
    qhupdate.set_defaults(__qhaction="update")
    qhdestroy.set_defaults(__qhaction="destroy")

    # subparser arguments are parsed as part of the main parser. or something.
    for plugin_name in plugins.keys():
        qhinit.add_argument(f"--{plugin_name}", action='store_true', dest=f"plugin_{plugin_name}")
        qhmake.add_argument(f"--{plugin_name}", action='store', dest=f"{plugin_name}_app_name")
        qhdescribe.add_argument(f"--{plugin_name}", action='store', dest=f"{plugin_name}_app_name")
        qhdestroy.add_argument(f"--{plugin_name}", action='store', dest=f"{plugin_name}_app_name")

    #################################################################3
    # find out if 'init' is the action.
    # hold on to unknown arguments to pass to their respective parser,
    # once the plugin is loaded
    _args = app_parser.parse_known_args()
    cli_args = vars(_args[0])
    logger.debug(f"first-pass {cli_args=}")
    action_cli_args = _args[1]
    logger.debug(f"first-pass {action_cli_args=}")
    action = cli_args['__qhaction']
    logger.debug(f"{action=}")
    config_file  = cli_args['config_file']

    ##################################################################
    # determine which plugin to use to create an instance of AppBase
    # the parser cannot contain app_name if init is the desired action* (why not?)
    # so we only add it after we know the action is anything other than.
    tgt_init_plugin = None
    if action == 'init':
        # find the plugin that was specified on the cli
        for k,v in cli_args.items():
            if k.startswith('plugin_') and v == True:
                tgt_init_plugin = k.split('_')[1]
                break
        logger.debug(f"{tgt_init_plugin=}")
        load = QHPlugin.load_plugin(tgt_init_plugin)
        app_class = load()
    #elif action == 'make':
    else:
        # make requires the --{plugin_name} flag
        tgt_plugin_name = None
        for arg,val in cli_args.items():
            if arg.endswith('app_name'):
                app_name = val
                tgt_plugin_name = arg.split('_app_name')[0]
        if app_name is None:
            print("need an app name")
            exit()
        load = QHPlugin.load_plugin(tgt_plugin_name)
        app_class = load()


######################################################################################3
# parse action's arguments
######################################################################################3
    if action == 'init':
        app_name = tgt_init_plugin
        app = app_class(app_name, config_file=None)
        init_parser = app.get_init_parser()
        init_args = init_parser.parse_args(action_cli_args)
        logger.debug(f"{init_args=}")
        return app.run_init(vars(init_args))

    elif action == 'make':
        app = app_class(app_name, config_file)
        make_parser = app.get_make_parser()
        make_args = make_parser.parse_args(action_cli_args)
        logger.debug(f"make_parser params: {make_args=}")
        return app.run_make(vars(make_args))
    elif action == 'describe':
        app = app_class(app_name, config_file)
        describe_parser = app.get_describe_parser()
        args = describe_parser.parse_args(action_cli_args)
        return app.run_describe(vars(args))
    elif action == 'destroy':
        app = app_class(app_name, config_file)
        destroy_parser = app.get_destroy_parser()
        args = destroy_parser.parse_args(action_cli_args)
        return app.run_destroy(vars(args))
    else:
        logger.error(f"No such action '{action}'")
        exit(QHExit.GENERAL_FAILURE)
    return None, None
    app = app_class(app)
    exit()

rc, fd1, fd2= main()
if fd1:
    sys.stdout.write(fd1 + "\n")
if fd2:
    sys.stderr.write(fd2 + "\n")
exit(rc)
