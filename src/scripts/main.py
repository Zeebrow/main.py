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

"""
main.py
1. Set up top-leel CLI arguments
2. Load all available plugins
3. Choose a plugin and load it
4. Add the plugin's arguments to the top-level parser
5. Create an instance of BaseApp with CLI args + config file
"""

logger = logging.getLogger()

def do_logging():
    global logger
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

def show_about():
    # TODO: cli flag
    print("""
<program>  Copyright (C) <year>  <name of author>
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
    """)

def cli_main():
#######################################################################################
# main argument parser
#######################################################################################
    app_parser = argparse.ArgumentParser(description="make easily managed hosts, quickly", add_help=False)
    app_parser.add_argument("-f", "--config-file", default=C.DEFAULT_CONFIG_FILEPATH, type=argparse.FileType('r'), required=False, help="Use an alternative configuration file to override the default.") # returns a called `open()` function
    app_parser.add_argument("-h", "--help",  dest='__help', action='store_true', required=False, help="Show this dialog and exit")
    app_parser.add_argument("--provider", default=None, dest='__provider', required=True, help="Choose which cloud provider to use to start your host.")
    app_parser.add_argument("--action", default=None, choices=["init", "make", "describe", "update", "destroy"], dest='__qhaction', required=True, help="Choose which action to take")

    _args = app_parser.parse_known_args()
    main_args = vars(_args[0])
    action = main_args['__qhaction']

    # load defaults from config file (such as log levels) - another time...
    do_logging()

    # handle help - another time...
    if main_args['__help']:
        app_parser.print_help()
        exit(1)
    

#######################################################################################
# fetch all plugins
#######################################################################################
    plugins = QHPlugin.load_all_plugins()
    logger.debug(f"{plugins=}")


#######################################################################################
# plugin argument parser
#######################################################################################
    load = QHPlugin.load_all_plugins()
    plugin_parser = load[main_args['__provider']]['parser']()()
    plugin_parser.add_parser_arguments(main_args['__qhaction'], app_parser)
    plugin_args = app_parser.parse_args()
    logger.debug(f"{plugin_args=}")

    app_class = load[main_args['__provider']]['app']()


#######################################################################################
# parse action's arguments
#######################################################################################
    if action == 'init':
        # every other action has a required 'app_name' argument, init uses its own provider name?! -_-
        app = app_class(main_args['__provider'])
        return app.run_init(vars(plugin_args))

    elif action == 'make':
        app = app_class(plugin_args.app_name)
        return app.run_make(vars(plugin_args))
    elif action == 'describe':
        app = app_class(plugin_args.app_name)
        return app.run_describe(vars(plugin_args))
    elif action == 'destroy':
        app = app_class(plugin_args.app_name)
        return app.run_destroy(vars(plugin_args))
    else:
        logger.error(f"No such action '{action}'")
        sys.exit(QHExit.GENERAL_FAILURE)

fd1, fd2, rc = cli_main()
if fd1:
    sys.stdout.write(fd1 + "\n")
if fd2:
    sys.stderr.write(fd2 + "\n")
sys.exit(rc)
