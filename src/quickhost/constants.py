from pathlib import Path

class APP_CONST:
    DEFAULT_CONFIG_FILEPATH = str(Path("/opt/etc/quickhost/quickhost.conf").absolute())
    DEFAULT_APP_NAME = 'quickhost'
    DEFAULT_OPEN_PORTS = ['22']
