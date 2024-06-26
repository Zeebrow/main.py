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
from pathlib import Path
import os
import logging
from time import perf_counter

logger = logging.getLogger(__name__)

TOTAL_RUNTIME = 0
MAX_FILE_SIZE_BYTES = 10_000_000  # ~10MB


def store_test_data(resource: str, action: str, response_data: dict, disable=True):
    if disable:
        return
    global TOTAL_RUNTIME
    t_start = perf_counter()
    cwd = Path(os.getcwd())
    if not (cwd.stem == 'aws' or cwd.stem == 'quickhost'):
        logger.debug(f"refusing to run from directory {cwd.stem}")
        return

    data_dir = cwd / "tests/data/mock-data"

    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    if not isinstance(response_data, dict):
        logger.debug(f"didn't get a dict, got a {type(response_data)}")
        return False

    d = Path(data_dir) / resource
    if not d.exists():
        d.mkdir()
    fp = d / f"{action}.json"

    if not fp.exists():
        newb = dict({action: []})
        with fp.open("w") as f:
            json.dump(newb, f)
    j = None
    if fp.stat().st_size >= MAX_FILE_SIZE_BYTES:
        logger.debug(f"{fp.stem} Max filesize reached")
    with fp.open("r") as g:
        print(fp.absolute())
        print(fp.absolute())
        print(fp.absolute())
        j = json.load(g)
        j[action].append(response_data)
    with fp.open("w") as h:
        json.dump(j, h)

    t_end = perf_counter()
    TOTAL_RUNTIME += t_end - t_start
    logger.debug("{:5f} of {:5f} sec to write test data to mock-data/{}/{} (now {:3.2f} Kib)".format(
        (t_end - t_start),
        TOTAL_RUNTIME,
        resource,
        fp.stem,
        fp.stat().st_size / 1024
    ))
    return True
