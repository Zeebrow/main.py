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

from .utilities import QHLogFormatter


class CliResponse(namedtuple('CliResponse', ['stdout', 'stderr', 'rc'])):
    __slots__ = ()


logger = logging.getLogger()


def do_logging(level: int):
    global logger

    if level > 2:
        level = 2
    verbosity = {
        0: logging.ERROR,
        1: logging.INFO,
        2: logging.DEBUG,
    }

    sh = logging.StreamHandler()
    logger.setLevel(verbosity[level])
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    sh.setFormatter(QHLogFormatter(color=True))
    logger.addHandler(sh)


def get_main_parser():
    parser = argparse.ArgumentParser(description="make a host, quickly", add_help=False)
    parser.add_argument("--help", "-h", action='store_true', required=False, help="help")
    parser.add_argument("-v", dest='verbosity', action='count', default=0, required=False, help="output verbosity")
    parser.add_argument("--version", action='store_true', required=False, help="display version information")
    return parser
