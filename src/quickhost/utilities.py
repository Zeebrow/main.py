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
import json
import urllib.request

def scrub_datetime(thing):
    """
    Remove all datetime objects from a dict, and convert them to a string
    """
    if isinstance(thing, dict):
        for k,v in thing.items():
            thing[k] = scrub_datetime(v)
    elif isinstance(thing, list):
        for i,a in enumerate(thing):
            thing[i] = scrub_datetime(a)
    elif isinstance(thing, datetime.datetime):
        thing = str(thing)
    else:
        return thing
    return thing

def get_my_public_ip() -> str:
    # what could possibly be better?!
    try:
        with urllib.request.urlopen("https://ipv4.icanhazip.com") as r:
            html = r.read()
            return html.decode('utf-8').strip() + "/32"
    except Exception:
        return input('Could not determine your public ip address (are you connected to the internet?). Enter it here (Ctrl^C to cancel): ')
