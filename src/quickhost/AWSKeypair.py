import logging
import shutil
from pathlib import Path
from tempfile import mkstemp

from botocore.exceptions import ClientError
#epiphany for if name=main
try:
    from .constants import *
except:
    from constants import *

logger = logging.getLogger(__name__)

class KP:
    def __init__(self, client: any, app_name: str, ssh_key_filepath: str, key_name=None, dry_run=True):
        self.client = client
        self.app_name = app_name
        self.ssh_key_filepath = ssh_key_filepath
        self.dry_run = dry_run
        self.key_name = key_name
        if not self.key_name:
            # not overridden by config
            self.key_name = app_name
        # we don't allow overriding key_id
        self._key_id = None
        self._fingerprint = None

    def __repr__(self):
        return str(self.key_id)
        #return str(self.key_name)

    # @@@naming
    def get_key_id(self) -> dict:
        """
        call aws to get existing ec2 key
        returns None if the ex2 key does not exist
        """
        try: 
            _existing_key = self.client.describe_key_pairs(
                KeyNames=[
                    self.app_name
                ],
                DryRun=self.dry_run,
                # @@@I think aws cli needs an update
                #IncludePublicKey=True
            )
        except ClientError:
            return None
        if len(_existing_key['KeyPairs']) > 1:
            logger.warning(f"WARN: Found more than 1 key pair named '{self.app_name}' in result set")
            print(_existing_key)
            return None
        self.key_id = _existing_key['KeyPairs'][0]['KeyPairId']
        self._fingerprint = _existing_key['KeyPairs'][0]['KeyFingerprint']
        del _existing_key
        return self.key_id

    def create(self) -> dict:
        """Make a new ec2 keypair named for app"""
        if self.ssh_key_filepath is None:
            # not overriden from config, set default
            tgt_file = Path(f"./{self.app_name}.pem")
        else:
            if not self.ssh_key_filepath.endswith('.pem'):
                tgt_file = Path(f"{self.ssh_key_filepath}.pem")
            else:
                tgt_file = Path(self.ssh_key_filepath)
        if tgt_file.exists():
            logger.error(f"pem file '{tgt_file.absolute()}' already exists")
            exit(1)

        _new_key = self.client.create_key_pair(
            KeyName=self.key_name,
            DryRun=self.dry_run,
            KeyType='rsa',
            TagSpecifications=[
                {
                    'ResourceType': 'key-pair',
                    'Tags': [
                        { 'Key': DEFAULT_APP_NAME, 'Value': self.app_name},
                    ]
                },
            ],
            # @@@Why is this param throwing errors, can't be shitty docs...
            #KeyFormat='pem'
        )

        # save pem
        with tgt_file.open('w') as pemf:
            pemf.writelines(_new_key['KeyMaterial'])
        print(f"saved private key to file '{tgt_file.absolute()}'")
        self.key_id = _new_key['KeyPairId']
        self._fingerprint = _new_key['KeyFingerprint']
        del _new_key
        return self.key_id

    def destroy(self) -> bool:
        if self._id is None:
            self._id = self.get_key_pair()['KeyPairId']
        try:
            _del_key = self.client.delete_key_pair(
                KeyName=self.app_name,
                KeyPairId=self._id,
                DryRun=self.dry_run
            )
            return True
        except ClientError as e:
            logger.warning(f"failed to delete keypair for app '{self.app_name}' (id: '{self._id}'):\n {e}")
            return False

    def update(self):
        """Not implemented"""
        pass

    def _get_private_key(self, to_file=None) -> None:
        """ 
        download ec2 keypair for appname and exits
        exit 0 if private key saved successfully with 0600 perm
        exit 1 if ec2 key named APP_NAME does not exist
        exit 2 if ec2 key exists but can't save
        exit 3 if bug
        """
        try: 

            with tgt_file.open('w') as pem:
                _existing_key = self.client.describe_key_pairs(
                    KeyNames=[
                        self.app_name
                    ],
                    DryRun=self.dry_run,
                )
                print(_existing_key)

        except PermissionError as pe:
            print(f"Could not open file ")
        except ClientError:
            print(f"No such ec2 key named '{self.app_name}'!")
            exit(1)
        if len(_existing_key['KeyPairs']) > 1:
            logger.warning(f"WARN: Found more than 1 key pair named '{self.app_name}' in result set")
            print(_existing_key)
            exit(3)
        exit(0)


if __name__ == '__main__':
    import boto3
    import json
    c = boto3.client('ec2')
    kp = KP(client=c, app_name='asdf', dry_run=False )
    #print(json.dumps(kp.get_key_pair(),indent=2))
    #print(kp.destroy())
    #print(json.dumps(kp.create(),indent=2))
    print()
    kp._get_private_key(to_file='mypem.pem')

