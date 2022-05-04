import boto3

from .cli_params import App
from .SG import SG


class AWSApp(App):
    def __init__(self):
        self.client = boto3.client("ec2")


    def create(self):
        _sg = SG()
        return _sg.sgid


    def destroy(self):
        pass
