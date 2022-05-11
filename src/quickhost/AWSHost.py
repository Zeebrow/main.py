from typing import List
import time
import logging
import json

import boto3

from .utilities import get_my_public_ip, convert_datetime_to_string
from .constants import *
from .cli_params import AppBase, AppConfigFileParser
from .SG import SG

logger = logging.getLogger(__name__)

#from .PropsBase import HostProps


class AWSHost:
    def __init__(self, client: any, ):
        self.client = client
        self.instance_config = instance_config
        self.sgid = None

    def new_instances(self, num_hosts:int, image_id:str, instance_type:str, sgid:str, subnet_id:str, app_name:str, userdata=None, dry_run=True):
        _run_instances_params = {
            'ImageId': image_id,
            'InstanceType':instance_type,
            'KeyName': self.instance_config.key_name,
            'Monitoring':{ 'Enabled': False },
            'MaxCount':int(num_hosts),
            'MinCount':1,
            'DisableApiTermination':False,
            'DryRun':dry_run,
            'InstanceInitiatedShutdownBehavior':'terminate',
            'NetworkInterfaces':[
                {
                    'AssociatePublicIpAddress': True,
                    'DeviceIndex': 0,
                    'SubnetId': self.instance_config.subnet_id,
                    'Groups': [
                        sgid
                    ],
                }
            ],
            'TagSpecifications':[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        { 'Key': DEFAULT_APP_NAME, 'Value': app_name},
                    ]
                },
            ],
        }
        if userdata:
            _run_instances_params['UserData'] = get_userdata(userdata)
        response = ec2.run_instances(**_run_instances_params)
        r_cleaned = convert_datetime_to_string(response)

        with open("instance-responses.json", 'w') as j:
            json.dump(r_cleaned, j, indent=2)
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

    def make_instances(self, num_hosts:int, instance_type:str, app_name:str, ports:List[int], cidrs:List[str], subnet_id: str, userdata=None, ami=None, dry_run=True):
        image_id=None
        if not ami:
            image_id = get_latest_image(dry_run)
        else:
            image_id = ami

        print(f"getting latest ami...", end='')
        print(f"done ({image_id})")
        print("making security group'...", end='')
        sgid = new_sg(
                app_name=app_name, 
                dry_run=dry_run)
        print(f"done ({sgid})")
        print(f"setting permissions...", end='')
        auth_sg(sgid=sgid, ports=ports, cidrs=cidrs, dry_run=dry_run)
        print("done")
        print(f"starting hosts...", end='')
        responses = new_instances(
            num_hosts=num_hosts,
            image_id=image_id,
            instance_type=instance_type,
            sgid=sgid,
            subnet_id=self.instance_config.subnet_id,
            app_name=app_name,
            dry_run=dry_run,
            userdata=userdata
        )
        #r_cleaned = convert_datetime_to_string(responses)
        #print(json.dumps(r_cleaned, indent=2))
        instance_ids = []
        for i in responses['Instances']:
            instance_ids.append(i['InstanceId'])
        return instance_ids


if __name__ == "__main__":
    params = {
            'num_hosts':1,
            'instance_type':'t3.nano', 
            'app_name': 'test_make_instances.py',
            'ports':[22],
            'cidrs':['123'],
            'subnet_id': self.instance_config.subnet_id,
            'dry_run':True,
            }
    make_instances(**params)

