patched_describe_sg = {
    "SecurityGroups": [
        {
            "Description": "test client.describe_security_groups patched response",
            "GroupName": "asdf",
            "IpPermissions": [
                {
                    "FromPort": 123,
                    "IpProtocol": "tcp",
                    "IpRanges": [
                        {
                            "CidrIp": "",
                            "Description": "made with quickhosts"
                            }
                        ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": [],
                    "ToPort": 123,
                    "UserIdGroupPairs": []
                    },
                {
                    "FromPort": 42,
                    "IpProtocol": "tcp",
                    "IpRanges": [
                        {
                            "CidrIp": "",
                            "Description": "made with quickhosts"
                            }
                        ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": [],
                    "ToPort": 42,
                    "UserIdGroupPairs": []
                    },
                {
                    "FromPort": 80,
                    "IpProtocol": "tcp",
                    "IpRanges": [
                        {
                            "CidrIp": "",
                            "Description": "made with quickhosts"
                            }
                        ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": [],
                    "ToPort": 80,
                    "UserIdGroupPairs": []
                    }
                ],
            "OwnerId": "188154480716",
            "GroupId": "sg-04bf04a4a22a9f07e",
            "IpPermissionsEgress": [
                {
                    "IpProtocol": "-1",
                    "IpRanges": [
                        {
                            "CidrIp": "1.2.3.4/24"
                            }
                        ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": [],
                    "UserIdGroupPairs": []
                    }
                ],
            "Tags": [
                {
                    "Key": "quickhost",
                    "Value": "asdf"
                    }
                ],
            "VpcId": "vpc-7c31a606"
            }
        ],
    "ResponseMetadata": {
        "RequestId": "1ba0c864-6a23-4a92-b5f9-b969dc95bbb0",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "1ba0c864-6a23-4a92-b5f9-b969dc95bbb0",
            "cache-control": "no-cache, no-store",
            "strict-transport-security": "max-age=31536000; includeSubDomains",
            "content-type": "text/xml;charset=UTF-8",
            "content-length": "1761",
            "date": "Wed, 18 May 2022 20:01:54 GMT",
            "server": "AmazonEC2"
            },
        "RetryAttempts": 0
        }
}

patched_describe_kp = {
  "KeyPairs": [
    {
      "KeyPairId": "key-0b4a1597913d76bd6",
      "KeyFingerprint": "40:86:26:62:9d:79:8a:40:09:41:23:fb:fa:ea:fe:7d:fb:ad:57:ed",
      "KeyName": "asdf",
      "KeyType": "rsa",
      "Tags": [
        {
          "Key": "quickhost",
          "Value": "asdf"
        }
      ]
    }
  ],
  "ResponseMetadata": {
    "RequestId": "b40c8248-355e-4301-987e-9fb5d058b6fc",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "x-amzn-requestid": "b40c8248-355e-4301-987e-9fb5d058b6fc",
      "cache-control": "no-cache, no-store",
      "strict-transport-security": "max-age=31536000; includeSubDomains",
      "content-type": "text/xml;charset=UTF-8",
      "content-length": "731",
      "date": "Sat, 21 May 2022 18:55:53 GMT",
      "server": "AmazonEC2"
    },
    "RetryAttempts": 0
  }
}

patched_describe_host = {
  "Reservations": [
    {
      "Groups": [],
      "Instances": [
        {
          "AmiLaunchIndex": 0,
          "ImageId": "ami-0b898040803850657",
          "InstanceId": "i-088642425e6548407",
          "InstanceType": "t2.micro",
          "KeyName": "asdf",
          "LaunchTime": "2022-05-20 21:50:31+00:00",
          "Monitoring": {
            "State": "disabled"
          },
          "Placement": {
            "AvailabilityZone": "us-east-1f",
            "GroupName": "",
            "Tenancy": "default"
          },
          "PrivateDnsName": "",
          "ProductCodes": [],
          "PublicDnsName": "",
          "State": {
            "Code": 48,
            "Name": "terminated"
          },
          "StateTransitionReason": "User initiated (2022-05-20 21:50:43 GMT)",
          "Architecture": "x86_64",
          "BlockDeviceMappings": [],
          "ClientToken": "422f1b1d-d0d5-4a8d-9889-1b4a58fa93ee",
          "EbsOptimized": False,
          "EnaSupport": True,
          "Hypervisor": "xen",
          "NetworkInterfaces": [],
          "RootDeviceName": "/dev/xvda",
          "RootDeviceType": "ebs",
          "SecurityGroups": [],
          "StateReason": {
            "Code": "Client.UserInitiatedShutdown",
            "Message": "Client.UserInitiatedShutdown: User initiated shutdown"
          },
          "Tags": [
            {
              "Key": "quickhost",
              "Value": "asdf"
            }
          ],
          "VirtualizationType": "hvm",
          "CpuOptions": {
            "CoreCount": 1,
            "ThreadsPerCore": 1
          },
          "CapacityReservationSpecification": {
            "CapacityReservationPreference": "open"
          },
          "HibernationOptions": {
            "Configured": False
          },
          "MetadataOptions": {
            "State": "pending",
            "HttpTokens": "optional",
            "HttpPutResponseHopLimit": 1,
            "HttpEndpoint": "enabled",
            "HttpProtocolIpv6": "disabled",
            "InstanceMetadataTags": "disabled"
          },
          "EnclaveOptions": {
            "Enabled": False
          },
          "PlatformDetails": "Linux/UNIX",
          "UsageOperation": "RunInstances",
          "UsageOperationUpdateTime": "2022-05-20 21:50:31+00:00",
          "MaintenanceOptions": {
            "AutoRecovery": "default"
          }
        }
      ],
      "OwnerId": "188154480716",
      "ReservationId": "r-071677cad2e61c193"
    },
    {
      "Groups": [],
      "Instances": [
        {
          "AmiLaunchIndex": 0,
          "ImageId": "ami-0b898040803850657",
          "InstanceId": "i-0f34a77c50806fff2",
          "InstanceType": "t2.micro",
          "KeyName": "asdf",
          "LaunchTime": "2022-05-20 22:22:41+00:00",
          "Monitoring": {
            "State": "disabled"
          },
          "Placement": {
            "AvailabilityZone": "us-east-1f",
            "GroupName": "",
            "Tenancy": "default"
          },
          "PrivateDnsName": "ip-172-31-0-121.ec2.internal",
          "PrivateIpAddress": "172.31.0.121",
          "ProductCodes": [],
          "PublicDnsName": "ec2-3-237-4-99.compute-1.amazonaws.com",
          "PublicIpAddress": "3.237.4.99",
          "State": {
            "Code": 16,
            "Name": "running"
          },
          "StateTransitionReason": "",
          "SubnetId": "subnet-03d71a20b7758e44b",
          "VpcId": "vpc-7c31a606",
          "Architecture": "x86_64",
          "BlockDeviceMappings": [
            {
              "DeviceName": "/dev/xvda",
              "Ebs": {
                "AttachTime": "2022-05-20 22:22:42+00:00",
                "DeleteOnTermination": True,
                "Status": "attached",
                "VolumeId": "vol-03feb2bbf4adedad1"
              }
            }
          ],
          "ClientToken": "bfd65b8e-0943-47b6-9313-938110ac22e4",
          "EbsOptimized": False,
          "EnaSupport": True,
          "Hypervisor": "xen",
          "NetworkInterfaces": [
            {
              "Association": {
                "IpOwnerId": "amazon",
                "PublicDnsName": "ec2-3-237-4-99.compute-1.amazonaws.com",
                "PublicIp": "3.237.4.99"
              },
              "Attachment": {
                "AttachTime": "2022-05-20 22:22:41+00:00",
                "AttachmentId": "eni-attach-085745631833049ed",
                "DeleteOnTermination": True,
                "DeviceIndex": 0,
                "Status": "attached",
                "NetworkCardIndex": 0
              },
              "Description": "",
              "Groups": [
                {
                  "GroupName": "asdf",
                  "GroupId": "sg-0c91f5ba8abbebc88"
                }
              ],
              "Ipv6Addresses": [],
              "MacAddress": "16:3f:67:8f:0b:09",
              "NetworkInterfaceId": "eni-08d24425cef4035a0",
              "OwnerId": "188154480716",
              "PrivateDnsName": "ip-172-31-0-121.ec2.internal",
              "PrivateIpAddress": "172.31.0.121",
              "PrivateIpAddresses": [
                {
                  "Association": {
                    "IpOwnerId": "amazon",
                    "PublicDnsName": "ec2-3-237-4-99.compute-1.amazonaws.com",
                    "PublicIp": "3.237.4.99"
                  },
                  "Primary": True,
                  "PrivateDnsName": "ip-172-31-0-121.ec2.internal",
                  "PrivateIpAddress": "172.31.0.121"
                }
              ],
              "SourceDestCheck": True,
              "Status": "in-use",
              "SubnetId": "subnet-03d71a20b7758e44b",
              "VpcId": "vpc-7c31a606",
              "InterfaceType": "interface"
            }
          ],
          "RootDeviceName": "/dev/xvda",
          "RootDeviceType": "ebs",
          "SecurityGroups": [
            {
              "GroupName": "asdf",
              "GroupId": "sg-0c91f5ba8abbebc88"
            }
          ],
          "SourceDestCheck": True,
          "Tags": [
            {
              "Key": "quickhost",
              "Value": "asdf"
            }
          ],
          "VirtualizationType": "hvm",
          "CpuOptions": {
            "CoreCount": 1,
            "ThreadsPerCore": 1
          },
          "CapacityReservationSpecification": {
            "CapacityReservationPreference": "open"
          },
          "HibernationOptions": {
            "Configured": False
          },
          "MetadataOptions": {
            "State": "applied",
            "HttpTokens": "optional",
            "HttpPutResponseHopLimit": 1,
            "HttpEndpoint": "enabled",
            "HttpProtocolIpv6": "disabled",
            "InstanceMetadataTags": "disabled"
          },
          "EnclaveOptions": {
            "Enabled": False
          },
          "PlatformDetails": "Linux/UNIX",
          "UsageOperation": "RunInstances",
          "UsageOperationUpdateTime": "2022-05-20 22:22:41+00:00",
          "PrivateDnsNameOptions": {
            "HostnameType": "ip-name",
            "EnableResourceNameDnsARecord": False,
            "EnableResourceNameDnsAAAARecord": False
          },
          "MaintenanceOptions": {
            "AutoRecovery": "default"
          }
        }
      ],
      "OwnerId": "188154480716",
      "ReservationId": "r-07bf6afc556ace526"
    }
  ],
  "ResponseMetadata": {
    "RequestId": "bf27fe42-3e60-44a6-a942-5e35bda7f3d6",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "x-amzn-requestid": "bf27fe42-3e60-44a6-a942-5e35bda7f3d6",
      "cache-control": "no-cache, no-store",
      "strict-transport-security": "max-age=31536000; includeSubDomains",
      "vary": "accept-encoding",
      "content-type": "text/xml;charset=UTF-8",
      "transfer-encoding": "chunked",
      "date": "Fri, 20 May 2022 22:23:44 GMT",
      "server": "AmazonEC2"
    },
    "RetryAttempts": 0
  }
}
