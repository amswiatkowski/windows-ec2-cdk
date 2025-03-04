from typing import Final

import boto3
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from mypy_boto3_ec2 import EC2Client
from windows_ec2.constants import EC2_KEY_NAME


class WindowsEC2Construct(Construct):
    _VPC_CIDR: Final[str] = '10.1.0.0/16'
    _RDP_PORT: Final[int] = 3389

    def __init__(self, scope: Construct, stack_id: str) -> None:
        super().__init__(scope, stack_id)

        self._stack = Stack.of(self)
        self.region = self._stack.region

        self._generate_key_pair()

        subnets = [
            ec2.SubnetConfiguration(name="public-subnet-1", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
            ec2.SubnetConfiguration(name="private-subnet-1", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24)
        ]
        self.vpc = ec2.Vpc(
            self,
            "ClientVPC",
            max_azs=2,
            nat_gateways=1,
            ip_addresses=ec2.IpAddresses.cidr(self._VPC_CIDR),
            subnet_configuration=subnets,
            restrict_default_security_group=True,  # TO
            enable_dns_support=True,
            enable_dns_hostnames=True)

        self.ec2_sg = ec2.SecurityGroup(self, "ClientSecurityGroup", vpc=self.vpc, allow_all_outbound=True)
        # Allow RDP access from the world. It's worth to limit it to you IP address or CIDR block
        self.ec2_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(self._RDP_PORT), "Allow RDP access from the world")

    def _generate_key_pair(self) -> None:
        ec2_client: EC2Client = boto3.client('ec2', region_name=self.region)
        ec2_client.delete_key_pair(KeyName=EC2_KEY_NAME)
        keypair = ec2_client.create_key_pair(KeyName=EC2_KEY_NAME)
        with open('client_ec2_key.pem', 'w', encoding='utf-8') as f:
            f.write(keypair.get('KeyMaterial'))
