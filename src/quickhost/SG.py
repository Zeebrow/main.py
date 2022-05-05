from typing import List, Union
from dataclasses import dataclass
import logging

import botocore.exceptions

from .constants import *

logger = logging.getLogger(__name__)

class SG:
    def __init__(self, client: any, app_name: str, vpc_id: str, ports: List[int], cidrs: List[str], dry_run: bool):
        self.client = client
        self.app_name = app_name
        self.vpc_id = vpc_id
        self.ports = ports
        self.cidrs = cidrs
        self.dry_run = dry_run
        self.sgid = None


    def get_security_group(self):
        # raw response
        # {'SecurityGroups': [{'Description': 'Made with love and care'
#             'GroupName': 'asdf'
#             'IpPermissions': [{'FromPort': 22
#             'IpProtocol': 'tcp'
#             'IpRanges': [{'CidrIp': '70.240.235.147/32'
#             'Description': 'made with quickhosts'}]
#             'Ipv6Ranges': []
#             'PrefixListIds': []
#             'ToPort': 22
#             'UserIdGroupPairs': []}]
#             'OwnerId': '188154480716'
#             'GroupId': 'sg-07b204811dd71f6c0'
#             'IpPermissionsEgress': [{'IpProtocol': '-1'
#             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
#             'Ipv6Ranges': []
#             'PrefixListIds': []
#             'UserIdGroupPairs': []}]
#             'Tags': [{'Key': 'app'
#             'Value': 'asdf'}]
#             'VpcId': 'vpc-7c31a606'}]
#             'ResponseMetadata': {'RequestId': '7a3d437b-795f-4166-b714-da6088a6744e'
#             'HTTPStatusCode': 200
#             'HTTPHeaders': {'x-amzn-requestid': '7a3d437b-795f-4166-b714-da6088a6744e'
#             'cache-control': 'no-cache
#             no-store'
#             'strict-transport-security': 'max-age=31536000; includeSubDomains'
#             'content-type': 'text/xml;charset=UTF-8'
#             'content-length': '1761'
#             'date': 'Thu
#             05 May 2022 18:20:56 GMT'
#             'server': 'AmazonEC2'}
#             'RetryAttempts': 0}}
        _dsg = None
        try:
            _dsg = self.client.describe_security_groups(
                    GroupNames=[self.app_name],
                    #VpcId=[self.vpc_id],
            )
        except botocore.exceptions.ClientError:
            logger.debug("security group does not exist!")
            return None
        if len(_dsg['SecurityGroups']) > 1:
            raise RuntimeError(f"More than 1 security group was found with the name '{self.app_name}': {_sg['GroupId'] for _sg in _dsg['SecurityGroups']}")
        return _dsg['SecurityGroups'][0]['GroupId']

    def create(self):
        print('creating sg...', end='')
        try:
            _sg = self.client.create_security_group(
                Description="Made by quickhost",
                GroupName=self.app_name,
                VpcId=self.vpc_id,
                TagSpecifications=[
                    {
                        'ResourceType': 'security-group',
                        'Tags': [
                            {
                                'Key': DEFAULT_APP_NAME,
                                'Value': self.app_name
                            }
                        ]
                    }
                ],
                DryRun=self.dry_run
            )
            print('done')
            return _sg['GroupId']
        except botocore.exceptions.ClientError:
            print('error')
            raise Exception(f"You already have a security group named '{self.app_name}', delete it first or use a different name.")

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
        response = self.client.authorize_security_group_ingress(
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


