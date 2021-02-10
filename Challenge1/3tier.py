import boto3
import os

# As a important components of 3-Tier architecture, I'm creating ELB, EC2 and RDS.
# Parameters are hardcoded.

def main():
    ### Create Key pair For EC2.
    ec2_client = boto3.client("ec2", region_name="eu-west-2")
    try:
        key_pair = ec2_client.create_key_pair(KeyName="test-key-pair")
        print(key_pair)
        private_key = key_pair["KeyMaterial"]
        print (private_key)

        # write private key to file with 400 permissions
        with os.fdopen(os.open("/vagrant/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)
    except Exception as e:
        print(e)
        print("key \"test-key-pair\" already exist.")

    ### Create EC2 Instance.
    ec2_resource = boto3.resource('ec2')
    try:
        ec2_instance_list = ec2_resource.create_instances(
            ImageId='ami-098828924dc89ea4a',
            InstanceType='t2.micro',
            KeyName='test-key-pair',
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'boto3_inst'
                        },
                    ]
                },
            ],
        )
        for ec2_instance in ec2_instance_list:
            for tag in ec2_instance.tags:
                if tag['Value'] == 'boto3_inst':
                    instance_id = ec2_instance.id
                    print(instance_id)
    except Exception as e:
        print(e)
        print("EC2 \"boto3_inst\" Unable to create.")

    #### Create RDS Postgres DB.
    db_identifier = 'boto3TestDB'
    rds = boto3.client('rds')
    try:
        rds.create_db_instance(DBInstanceIdentifier=db_identifier,
                               DBInstanceClass='db.m3.2xlarge',
                               DBName='testDB',
                               Engine='postgres',
                               StorageType='gp2',
                               AllocatedStorage=200,
                               StorageEncrypted=True,
                               AutoMinorVersionUpgrade=True,
                               MultiAZ=False,
                               MasterUsername='Master',
                               MasterUserPassword='Master123',
                               Tags=[{'Key': 'Name', 'Value': 'Hawaii'}])
        print 'Starting RDS instance with ID: %s' % db_identifier
    except botocore.exceptions.ClientError as e:
        if 'DBInstanceAlreadyExists' in e.message:
            print 'DB instance %s already exists.' % db_identifier
        else:
            raise

    #### Create ELB for 3-tier stack.
    alb_resource = client.create_load_balancer(
    AvailabilityZones=[
        'eu-west-2',
    ],
    Listeners=[
        {
            'InstancePort': 80,
            'InstanceProtocol': 'HTTP',
            'LoadBalancerPort': 80,
            'Protocol': 'HTTP',
        },
    ],
    LoadBalancerName='my-test-lb',
    )
    #print(response)

### Initiating main
if __name__ == '__main__':
    main()