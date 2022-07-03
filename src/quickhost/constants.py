from pathlib import Path

class APP_CONST:
    #DEFAULT_CONFIG_FILEPATH = str(Path("/opt/etc/quickhost/quickhost.conf").absolute()) # XD
    DEFAULT_CONFIG_FILEPATH = str(Path().home() / ".local/etc/quickhost.conf")
    DEFAULT_SSH_KEY_FILE_DIR = Path.home() / '.ssh'
    DEFAULT_APP_NAME = 'quickhost'
    DEFAULT_OPEN_PORTS = ['22']
    DEFAULT_VPC_CIDR = '172.16.0.0/16'
    DEFAULT_SUBNET_CIDR = '172.16.0.0/24'

class QHExit:
    OK = 0
    GENERAL_FAILURE = 1
    KNOWN_ISSUE = 2
    # 2x - security-related
    NOT_QH_USER = 21
    
