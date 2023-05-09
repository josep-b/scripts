import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    
    instances = response['Reservations']
    
    instance_owner_mapping = []
    
    for reservation in instances:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            owner = get_instance_owner(instance)
            instance_owner_mapping.append({'InstanceId': instance_id, 'Owner': owner})
    
    print(instance_owner_mapping)
    return instance_owner_mapping

def get_instance_owner(instance):
    for tag in instance['Tags']:
        if tag['Key'] == 'Owner':
            return tag['Value']
    return 'N/A'


# command for instance

aws ec2 describe-instances --query 'Reservations[].Instances[].{InstanceID:InstanceId, Owner:Tags[?Key==`Owner`].Value | [0]}' --output table > instances.txt
