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

import sys
import logging
from typing import Type

from quickhost import Cli, QHPlugin, Plugin, AppBase, ParserBase, CliResponse

"""
main.py
`console-script` entrypoint for package 'quickhost'
"""

logger = logging.getLogger()


def cli_main() -> CliResponse:
    plugins: dict[str, Plugin] = QHPlugin.load_all_plugins()
    app_parser = Cli.get_main_parser()  # subject to change

    main_subparser = app_parser.add_subparsers(dest='plugin')
    for name, p in plugins.items():
        plugin_subparser = main_subparser.add_parser(name)
        plugin_parser_class: ParserBase = p.parser
        # @@@ pyright smells something smelly with my world-class annotations
        # type(plugin_parser_class)=<class 'type'>
        # type(plugin_parser_class())=<class 'quickhost_null.NullParser.NullParser'>
        # print(f"{type(plugin_parser_class)=}")
        # print(f"{type(plugin_parser_class())=}")  # pyright: ignore
        plugin_parser_class().add_subparsers(plugin_subparser)  # pyright: ignore

    args = vars(app_parser.parse_args())

    Cli.do_logging(args['verbosity'])
    logger.debug("cli args={}".format(args))

    if args['version']:
        from importlib.metadata import version
        return CliResponse(version('quickhost'), '', 0)

    if dict(plugins) == {}:
        app_parser.print_help()
        return CliResponse('', "No plugins are installed! Try pip install --user quickhost-aws", 1)

    tgt_plugin = args.pop('plugin')
    logger.debug(f"{tgt_plugin=}")
    if tgt_plugin is None:
        app_parser.print_help()
        return CliResponse('', f"Provide a plugin {[k for k in plugins.keys()]}", 1)

    app_name = None  # @@@
    if 'app_name' in args.keys():  # @@@
        app_name = args.pop("app_name")  # @@@
    logger.debug(f"{app_name=}")
    action = args.pop(tgt_plugin)
    logger.debug(f"{action=}")
    app_class: AppBase = plugins[tgt_plugin].app
    app_instance: Type[AppBase] = app_class(app_name)  # pyright: ignore

    match action:
        case 'init':
            return app_instance.plugin_init(args)  # pyright: ignore
        case 'make':
            return app_instance.create(args)  # pyright: ignore
        case 'describe':
            return app_instance.describe(args)  # pyright: ignore
        case 'destroy':
            return app_instance.destroy(args)  # pyright: ignore
        case 'update':
            return app_instance.update(args)  # pyright: ignore
        case 'list-all':
            return app_class.list_all()  # pyright: ignore
        case 'destroy-all':
            return app_class.destroy_all()  # pyright: ignore
        case 'destroy-plugin':
            return app_instance.plugin_destroy(args)  # pyright: ignore
        case None:
            app_parser.print_help()
            return CliResponse('', f"No action provided (try quickhost {tgt_plugin} -h)", 1)
        case _:
            app_parser.print_help()
            return CliResponse('', f"Invalid action: '{action}'", 1)


fd1, fd2, rc = cli_main()
if fd1:
    sys.stdout.write("\033[32m{}\033[0m".format(fd1) + "\n")
if fd2:
    sys.stderr.write("\033[31mERROR:\033[0m" + fd2 + "\n")
raise SystemExit(rc)
