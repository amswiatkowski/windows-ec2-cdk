#!/usr/bin/env python3
import os

from aws_cdk import App, Environment
from boto3 import client, session
from windows_ec2.utils.utils import get_stack_name
from windows_ec2.windows_ec2_stack import WindowsEC2Stack

account = client('sts').get_caller_identity()['Account']
region = session.Session().region_name
app = App()
windows_ec2_stack = WindowsEC2Stack(
    app,
    get_stack_name(),
    description='Complete Windows EC2 Stack',
    env=Environment(account=os.environ.get('AWS_DEFAULT_ACCOUNT', account), region=os.environ.get('AWS_DEFAULT_REGION', region)),
)
app.synth()
