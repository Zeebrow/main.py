from typing import List
import time
import logging
import json
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from .utilities import get_my_public_ip, convert_datetime_to_string
from .constants import *
from .cli_params import AppBase, AppConfigFileParser
from .SG import SG

logger = logging.getLogger(__name__)

#from .PropsBase import HostProps



class AWSHost:
    def __init__(self, client: any, app_name, num_hosts, image_id, instance_type, sgid, subnet_id, userdata, dry_run, key_name=None ):
        self.client = client
        self.app_name=app_name
        self.num_hosts=num_hosts
        self.image_id=image_id
        self.instance_type=instance_type
        self.sgid=sgid
        self.subnet_id=subnet_id
        self.key_name = key_name
        if key_name is None:
            self.key_name = app_name
        self.userdata=userdata
        self.dry_run=dry_run

    @classmethod
    def get_latest_image(self, client=None):
        """
        Get the latest amazon linux 2 ami
        TODO: see source-aliases and make an Ubuntu option
        """
        response = client.describe_images(
            Filters=[
                {
                    'Name': 'name',
                    'Values': [ 'amzn2-ami-hvm-2.0.????????-x86_64-gp2', ]
                },
                {
                    'Name': 'state',
                    'Values': [ 'available', ]
                },
            ],
            IncludeDeprecated=False,
            DryRun=False
        )

        sortedimages = sorted(response['Images'], key=lambda x: datetime.strptime(x['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        return sortedimages[-1]['ImageId']

    def describe(self):
        _app_hosts = self.client.describe_instances(
            Filters=[
                { 'Name': f"tag:{DEFAULT_APP_NAME}", 'Values': [ self.app_name, ] },
            ],
            DryRun=False,
            # TODO/figure out
            MaxResults=10,
            #NextToken='string'
        )
        print(_app_hosts)
        return 


    def new_instances(self):
        ## this was moved from __init__ after causing describe() problems
        if self.image_id is None:
            print("No ami specified, getting latest al2...", end='')
            self.image_id = self.get_latest_image()
            print("done ({self.ami})")
        ##
        print(f"starting hosts...")
        _run_instances_params = {
            'ImageId': self.image_id,
            'InstanceType': self.instance_type,
            'KeyName': self.key_name,
            'Monitoring':{ 'Enabled': False },
            'MaxCount':int(self.num_hosts),
            'MinCount':1,
            'DisableApiTermination':False,
            'DryRun':self.dry_run,
            'InstanceInitiatedShutdownBehavior':'terminate',
            'NetworkInterfaces':[
                {
                    'AssociatePublicIpAddress': True,
                    'DeviceIndex': 0,
                    'SubnetId': self.subnet_id,
                    'Groups': [
                        self.sgid
                    ],
                }
            ],
            'TagSpecifications':[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        { 'Key': DEFAULT_APP_NAME, 'Value': self.app_name},
                    ]
                },
            ],
        }
        if self.userdata:
            _run_instances_params['UserData'] = self.get_userdata(userdata)
        response = self.client.run_instances(**_run_instances_params)
        r_cleaned = convert_datetime_to_string(response)

        for i in response['Instances']:
            print()
            print('--------------------')
            print(f"instance id: {i['InstanceId']}")
            print(f"security groups: {i['SecurityGroups']}")
            print('--------------------')
        time.sleep(1)
        return response

    # this is stupid. why?
    def get_userdata(self, filename: str):
        data=None
        with open(filename, 'r') as ud:
            data = ud.read()
        return data

    def create(self):
        self.new_instances()


