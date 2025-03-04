#!/usr/bin/env python
# pylint: disable=wrong-import-position
import inspect
import os.path
import sys

import boto3
from mypy_boto3_ec2 import EC2Client

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), '../'))

from windows_ec2.constants import EC2_KEY_NAME


def clean_old_keys() -> None:
    ec2_client: EC2Client = boto3.client('ec2', region_name=os.environ['REGION'])
    ec2_client.delete_key_pair(KeyName=EC2_KEY_NAME)


if __name__ == '__main__':
    clean_old_keys()
