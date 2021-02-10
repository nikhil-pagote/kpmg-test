import urllib.request

# There is no direct method in boto3 to fetch all metadata of ec2 instance. We need to fetch required metadata of EC2 instance as required. 
# I had avoided using 3rd part python module to fetch EC2 MetaData

def main():
    #Below code fetch Instance ID 
    instanceID = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
    print(instanceID)

# Trigger main constructor.
if __name__ == '__main__':
    main()