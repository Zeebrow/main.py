from typing import List
from dataclasses import dataclass

from .utilities import get_my_public_ip

@dataclass(init=True)
class CLIParams:
    userdata: str
    ami: str
    num_hosts: int
    instance_type: str
    app_name: str
    ports: List[int]
    cidrs: List[str]
    dry_run: bool = True


def parse_cli_params(args):
    ips = []
    ips.append(get_my_public_ip() + "/32")

    params = {
        'userdata': args.userdata,
        'ami': args.ami,
        'num_hosts':args.number_of_hosts,
        'instance_type': args.instance_type, 
        'app_name': args.app_name,
        'ports': args.port,
        'cidrs': ips,
        'dry_run': not args.not_dry_run
    }
    return params 

