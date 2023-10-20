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
import logging
from collections import namedtuple

from .QuickhostPlugin import QHPlugin
from .utilities import QHLogFormatter
from .quickhost_app_base import AppBase


class CliResponse(namedtuple('CliResponse', ['stdout', 'stderr', 'rc'])):
    __slots__ = ()


logger = logging.getLogger()


def do_logging(level: int):
    if not level:
        level = 0
    if level > 2:
        level = 2
    verbosity = {
        0: logging.ERROR,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    global logger

    sh = logging.StreamHandler()
    logger.setLevel(verbosity[level])
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    sh.setFormatter(QHLogFormatter(color=True))
    logger.addHandler(sh)


def get_main_parser():
    parser = argparse.ArgumentParser(description="make a proxmox-ve host, quickly", add_help=False)
    parser.add_argument("--help", "-h", action='store_true', required=False, help="help")
    parser.add_argument("-v", dest='verbosity', action='count', default=0, required=False, help="output verbosity")
    parser.add_argument("--version", action='store_true', required=False, help="display version information")
    return parser


def cli(plugin_name: str) -> CliResponse:
    """
    Load a plugin when you know that it is available on your PYTHONPATH.
    Use for writing plugin shortcut scripts, such as 'quickhost-<plugin_name>'
    """
    plugin = QHPlugin.try_load_plugin(plugin_name=plugin_name)
    app_parser = get_main_parser()
    main_args, plugin_args = app_parser.parse_known_args()
    main_args = vars(main_args)

    plugin.parser().add_subparsers(app_parser)  # pyright: ignore

    #############################
    # handle main_args
    do_logging(main_args['verbosity'])

    if main_args['version']:
        from importlib.metadata import version
        qh_ver = version('quickhost')
        plugin_ver = version(f"quickhost-{plugin_name}")
        return CliResponse(f"quickhost:\t{qh_ver}\nquickhost-{plugin_name}:\t{plugin_ver}", '', 0)

    # we can't know where exactly a -h was passed, only whether it was or not.
    # so we have to wait until the action (init, make, ..) is determined
    if main_args['help'] and plugin_args != []:
        # help for a particular action.
        # pass along the -h to subcommand
        # if the subcommand isn't valid, the list of choices are provided
        plugin_args.append('-h')
    elif main_args['help'] and plugin_args == []:
        # help for the plugin
        # no plugin args were passed, but help is requested so exit (0)
        app_parser.print_help()
        return CliResponse('', '', 0)
    elif not main_args['help'] and plugin_args == []:
        # help for the plugin
        # a blank command line was passed
        app_parser.print_usage()
        return CliResponse('', f"No plugin arguments were specified (try quickhost-{plugin.name} -h)", 1)

    #
    #############################

    plugin_parser = argparse.ArgumentParser()
    plugin.parser().add_subparsers(plugin_parser)  # pyright: ignore
    args = vars(plugin_parser.parse_args(plugin_args))

    action = args.pop(plugin_name)
    logger.debug("action={}".format(action))

    app_class: AppBase = plugin.app
    app_instance: AppBase = app_class(plugin.name)  # pyright: ignore

    if action == 'init':
        return app_instance.plugin_init(args)  # pyright: ignore
    elif action == 'make':
        return app_instance.create(args)  # pyright: ignore
    elif action == 'describe':
        return app_instance.describe(args)  # pyright: ignore
    elif action == 'destroy':
        return app_instance.destroy(args)  # pyright: ignore
    elif action == 'update':
        return app_instance.update(args)  # pyright: ignore
    elif action == 'list-all':
        return app_class.list_all()  # pyright: ignore
    elif action == 'destroy-all':
        return app_class.destroy_all()  # pyright: ignore
    elif action == 'destroy-plugin':
        return app_instance.plugin_destroy(args)  # pyright: ignore
    elif action == 'help':
        # @@@want: something for the Cobra-style commander users
        app_parser.print_help()
        return CliResponse('', 'For help on a specific action, use -h.', 1)
    elif action is None:
        # unreachable
        app_parser.print_help()
        return CliResponse('', "Bug! action was 'None'", 1)
    else:
        app_parser.print_help()
        return CliResponse('', f"Invalid action: '{action}'", 1)
