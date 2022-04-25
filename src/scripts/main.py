#!/usr/bin/env python3
import json
import argparse
import sys

def do_args():
    parser = argparse.ArgumentParser(description="make a bunch of ec2 servers, relatively quickly")

    ####### make-instances.py
    parser.add_argument("-y", "--not-dry-run", required=False, action='store_true', help="starts hosts when set")
    parser.add_argument("-c", "--number-of-hosts", required=False, default=1, help="number of hosts to create")
    parser.add_argument("-n", "--app-name", required=True, help="Name the group of hosts you're creating (remember, there is no state!)")
    parser.add_argument("--instance-type", required=False, default="t3.micro", help="change the type of instance to launch")
    parser.add_argument("--ami", required=False, default=None, help="change the ami to launch, see source-aliases for getting lastest")
    parser.add_argument("-u", "--userdata", required=False, default=None, help="path to optional userdata file")

    parser.add_argument_group("security group options", "modify the resulting security group with extra permissions. Default is locked down.")
    # todo - fix problem where specifying -p 22 throws error
    parser.add_argument("-p", "--port", required=False, action='append', default=[22], help="add an open tcp port to security group")
    parser.add_argument("--ip", required=False, action='append', help="additional ipv4 to allow through security group. if a cidr is not included, it is assumed to be /32")

    args = parser.parse_args()
    # prevents python from freaking out when the command is invoked with no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args

def build_cmd(args):
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


if __name__ == "__main__":
    args = do_args()
    params = build_cmd(args)
    print(params)
    # leftovers from the original script
    #make_instances(**params)
    #print("main - waiting for reservations...")
    #r = wait_for_reservations(args.app_name)



