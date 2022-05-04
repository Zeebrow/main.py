from typing import List, Union
from dataclasses import dataclass

from .constants import *

class SG:
    def __init__(self, client: any, vpc_id: str, ports: List[int], cidrs: List[str], dry_run: bool):
        self.client = client
        if (config is None) or (app_props is None):
            raise Exception('SG got no config')
        print(app_props)
        self.vpc_id = vpc_id
        self.ports = ports
        self.cidrs = cidrs
        self.group_name = group_name
        self.dry_run = dry_run
        self.get_security_group()
        exit()

        if not self.sgid:
            self.sgid = self.create()
        self.add_ingress(ports=ports, cidrs=cidrs)
        if not config.ports:
            self.ports = DEFAULT_SG_PORTS
        else:
            self.ports = self.ports = config.ports
        if not config.cidrs:
            self.cidrs = DEFAULT_SG_PORTS
        else:
            self.cidrs = self.cidrs = config.cidrs

    def get_security_group(self):
        _dsg = self.client.describe_security_groups(
                GroupName=self.group_name,
                VpcId=VPCID,
        )

    def create(self):
        print('creating sg...', end='')
        try:
            _sg = self.client.create_security_group(
                Description="Made by quickhost",
                GroupName=self.group_name,
                VpcId=VPCID,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': DEFAULT_APP_NAME,
                                'Value': group_name
                            }
                        ]
                    }
                ],
                DryRun=dry_run
            )
            print('done')
            return sg['GroupId']
        except be.ClientError:
            print('error')
            raise QHRuntimeError("You already have a security group (app) named '{self.group_name}', delete it first or use a different name.")

    def delete(self):
        pass

    def add_ingress(self, ports: List[int], cidrs:List[str]):
        perms = []
        for port in ports:
            perms.append({
                'FromPort': int(port),
                'IpProtocol': 'tcp',
                'IpRanges': [ { 'CidrIp': cidr, 'Description': 'made with quickhosts' } for cidr in cidrs ],
                'ToPort': int(port),
            })
        response = ec2.authorize_security_group_ingress(
            GroupId=self.sgid,
            IpPermissions=perms,
            DryRun=self.dry_run,
        )

    # example _sg
#    {
#      "GroupId": "sg-0b107cb50178800f0",
#      "ResponseMetadata": {
#        "RequestId": "4d52663e-660e-4c0b-b02a-f9ccfdd6b9a0",
#        "HTTPStatusCode": 200,
#        "HTTPHeaders": {
#          "x-amzn-requestid": "4d52663e-660e-4c0b-b02a-f9ccfdd6b9a0",
#          "cache-control": "no-cache, no-store",
#          "strict-transport-security": "max-age=31536000; includeSubDomains",
#          "content-type": "text/xml;charset=UTF-8",
#          "content-length": "283",
#          "date": "Wed, 23 Mar 2022 19:45:04 GMT",
#          "server": "AmazonEC2"
#        },
#        "RetryAttempts": 0
#      }
#    }


