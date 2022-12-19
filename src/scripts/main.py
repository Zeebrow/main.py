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

from quickhost import  APP_CONST as C, QHPlugin, AppBase, ParserBase

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
    plugins = QHPlugin.load_all_plugins()
#######################################################################################
# main argument parser
#######################################################################################
    app_parser = argparse.ArgumentParser(description="make easily managed hosts, quickly")
    app_parser.add_argument("-f", "--config-file", default=C.DEFAULT_CONFIG_FILEPATH, type=argparse.FileType('r'), required=False, help="Use an alternative configuration file to override the default.") # returns a called `open()` function
    # app_parser.add_argument("-h", "--help",  dest='help', action='store_true', required=False, help="Show this dialog and exit")
    main_subparser = app_parser.add_subparsers(dest='main')
    for k,v in plugins.items():
        plugin_subparser = main_subparser.add_parser(k)
        plugin_parser_class: ParserBase = v['parser']()()
        plugin_parser_class.add_subparsers(plugin_subparser)
    
    # load defaults from config file (such as log levels) - another time...
    do_logging()

    args = vars(app_parser.parse_args())

    [print(f"{k}: {v}") for k,v in args.items()]
    tgt_plugin = args.pop("main")
    app_name = None #@@@
    if 'app_name' in args.keys(): #@@@
        app_name = args.pop("app_name") #@@@
    action = args.pop(tgt_plugin)
    app_class: AppBase = plugins[tgt_plugin]['app']()(app_name)

    match action:
        case 'init':
            return app_class.plugin_init(args)
        case 'make':
            return app_class.create(args)
        case 'describe':
            return app_class.describe(args)
        case 'destroy':
            return app_class.destroy(args)
        case 'update':
            return app_class.update(args)

fd1, fd2, rc = cli_main()
if fd1:
    sys.stdout.write(fd1 + "\n")
if fd2:
    sys.stderr.write(fd2 + "\n")
sys.exit(rc)

