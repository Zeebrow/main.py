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

import argparse
import sys
import logging

from quickhost import  APP_CONST as C, QHPlugin, AppBase, ParserBase, QHLogFormatter

"""
main.py
1. Set up top-leel CLI arguments
2. Load all available plugins
3. Choose a plugin and load it
4. Add the plugin's arguments to the top-level parser
5. Create an instance of BaseApp with CLI args + config file
"""

logger = logging.getLogger()

def do_logging(level="AAAAAAAAAA ARGPARSE WHY ARE YOU LIKE THIS"):
    global logger
    sh = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    sh.setFormatter(QHLogFormatter(color=True))
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
    plugins = QHPlugin.load_all_plugins()
#######################################################################################
# main argument parser
#######################################################################################
    app_parser = argparse.ArgumentParser(description="make easily managed hosts, quickly", add_help=False)
    app_parser.add_argument("-h", action='store_true', required=False, help="help")

    _tempargs = app_parser.parse_known_args()
    do_logging()

    main_subparser = app_parser.add_subparsers(dest='main')
    for k,v in plugins.items():
        plugin_subparser = main_subparser.add_parser(k)
        plugin_parser_class: ParserBase = v['parser']()()
        plugin_parser_class.add_subparsers(plugin_subparser)
    
    args = vars(app_parser.parse_args())

    tgt_plugin = args.pop("main")
    if tgt_plugin is None:
        app_parser.print_help()
        exit(1)
    app_name = None #@@@
    if 'app_name' in args.keys(): #@@@
        app_name = args.pop("app_name") #@@@
    action = args.pop(tgt_plugin)
    app_class: AppBase = plugins[tgt_plugin]['app']()
    app_instance: AppBase = app_class(app_name)

    match action:
        case 'init':
            return app_instance.plugin_init(args)
        case 'make':
            return app_instance.create(args)
        case 'describe':
            return app_instance.describe(args)
        case 'destroy':
            return app_instance.destroy(args)
        case 'update':
            return app_instance.update(args)
        case 'list-all':
            return app_class.list_all()
        case 'destroy-all':
            logger.info("Destroy all {} apps".format(app_class.__name__))
            if not args['yes']:
                are_you_sure = input("Are you sure? (y/N)")
                if are_you_sure not in ["y", "Y", "yes", "YES"]:
                    print("Aborted")
                    logger.info("User aborted.")
                    exit(0)
            return app_class.destroy_all()
        case 'destroy-plugin':
            logger.info("Uninstalling plugin '{}'".format(app_class.__name__))
            app_instance.plugin_destroy(args)
            exit()

fd1, fd2, rc = cli_main()
if fd1:
    sys.stdout.write("\033[32m{}\033[0m".format(fd1) + "\n")
if fd2:
    sys.stderr.write("\033[31mERROR:\033[0m" + fd2 + "\n")
sys.exit(rc)

