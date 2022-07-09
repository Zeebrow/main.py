import json
from pathlib import Path
import os
import logging
from time import perf_counter

logger = logging.getLogger(__name__)

TOTAL_RUNTIME = 0
MAX_FILE_SIZE_BYTES = 10_000_000 #~10MB

def store_test_data(resource: str, action: str, response_data: dict):
    global TOTAL_RUNTIME
    t_start = perf_counter()
    cwd = Path(os.getcwd())
    if not (cwd.stem == 'aws' or cwd.stem == 'quickhost'): 
        logger.debug(f"refusing to run from directory {cwd.stem}")
        return

    data_dir = cwd/"tests/data/mock-data"

    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    if type(response_data) != type({}):
        logger.debug(f"didn't get a dict, got a {type(response)}")
        return False

    d = Path(data_dir) / resource 
    if not d.exists():
        d.mkdir()
    fp = d / f"{action}.json"

    if not fp.exists():
        newb = dict({action: []})
        print(newb)
        with fp.open("w") as f:
            json.dump(newb, f)
    j = None
    if fp.stat().st_size >= MAX_FILE_SIZE_BYTES:
        logger.debug(f"{fp.stem} Max filesize reached")
    with fp.open("r") as g:
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
        fp.stat().st_size/1024
    ))
    return True
    
    

if __name__ == '__main__':
    store_test_data(resource='blabla', action='test', response_data={'data':'True'})

    @get_test_data
    def asdf(a):
        print(f'asdf: {a}')
        return
    asdf('asddfasdfasdf')

    class A:
        def dostuff():
            print('doin stuff')
            return
        
