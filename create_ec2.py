import boto3

def create_security_group(name, desc, inIpPermissions=[], eIpPermissions=[]):
    ec2 = boto3.client('ec2')
    response = ec2.create_security_group(
        GroupName=name,
        Description=desc
    )
    security_group_id = response['GroupId']
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=inIpPermissions
    )
    data = ec2.authorize_security_group_egress(
        GroupId=security_group_id,
        IpPermissions=eIpPermissions
    )

def create_key_pair(name):
    ec2 = boto3.client('ec2')
    response = ec2.create_key_pair(
        KeyName=name
    )

def create_ec2(amiId, keyName, sgName, instType='t1.micro', minInst=1, maxInst=1):
    ec2 = boto3.client('ec2')
    instances = ec2.run_instances(
        ImageId=amiId,
        InstanceType=instType,
        KeyName=keyName,
        MinCount=minInst,
        MaxCount=maxInst,
        SecurityGroups=[sgName]
    )

if __name__ == "__main__":
    sgName = 'Open'
    sgDesc = 'Open from and to anywhere through any protocol'
    ipPermissions = [
        {
            'IpProtocol': '-1',
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
    create_security_group(sgName, sgDesc, ipPermissions, ipPermissions)

    keyName = 'cs-gy-9223'
    create_key_pair(keyName)

    amiId = 'ami-0c7217cdde317cfec' # Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
    create_ec2(amiId, keyName, sgName)