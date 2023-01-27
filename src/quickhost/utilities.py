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

import datetime
import logging
import urllib.request


def scrub_datetime(thing):
    """
    Remove all datetime objects from a dict, and convert them to a string
    """
    if isinstance(thing, dict):
        for k, v in thing.items():
            thing[k] = scrub_datetime(v)
    elif isinstance(thing, list):
        for i, a in enumerate(thing):
            thing[i] = scrub_datetime(a)
    elif isinstance(thing, datetime.datetime):
        thing = str(thing)
    else:
        return thing
    return thing


# @@@ testme
def get_my_public_ip() -> str:
    # what could possibly be better?!
    try:
        with urllib.request.urlopen("https://ipv4.icanhazip.com") as r:
            html = r.read()
            return html.decode('utf-8').strip() + "/32"
    except Exception:
        return input('Could not determine your public ip address (are you connected to the internet?). Enter it here (Ctrl^C to cancel): ')


class QHLogFormatter(logging.Formatter):
    """
    Shamelessly pilfered from
    https://stackoverflow.com/questions/14844970/modifying-logging-message-format-based-on-message-logging-level-in-python3#14859558
    """
    ErrorFormat = '%(levelname)s: %(message)s'
    CriticalFormat = ErrorFormat
    WarningFormat = ErrorFormat
    InfoFormat = ErrorFormat
    DebugFormat = '%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s'
    ErrorFormatColor = '\033[31m%(levelname)s:\033[0m %(message)s'
    CriticalFormatColor = ErrorFormatColor
    WarningFormatColor = '\033[93m%(levelname)s:\033[0m %(message)s'
    InfoFormatColor = '\033[33m%(levelname)s:\033[0m %(message)s'
    DebugFormatColor = '\033[94m%(asctime)s : %(name)s : %(funcName)s : %(levelname)s:\033[0m %(message)s'

    def __init__(self, color=False):
        self.colored_output = color
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):
        # orig_fmt = self._style._fmt
        if self.colored_output:
            match record.levelno:
                case logging.DEBUG:
                    self._style._fmt = QHLogFormatter.DebugFormatColor
                case logging.INFO:
                    self._style._fmt = QHLogFormatter.InfoFormatColor
                case logging.WARNING:
                    self._style._fmt = QHLogFormatter.WarningFormatColor
                case (logging.ERROR | logging.CRITICAL):
                    self._style._fmt = QHLogFormatter.ErrorFormatColor
        else:
            match record.levelno:
                case logging.DEBUG:
                    self._style._fmt = QHLogFormatter.DebugFormat
                case logging.INFO:
                    self._style._fmt = QHLogFormatter.InfoFormat
                case logging.WARNING:
                    self._style._fmt = QHLogFormatter.WarningFormat
                case (logging.ERROR | logging.CRITICAL):
                    self._style._fmt = QHLogFormatter.ErrorFormat
        return super().format(record)
