# AWS config
AWS_ACCESS_KEY = 'your access key'
AWS_SECRET_KEY = 'your secret key'

CLOUD_NAME = 'cloud'
REGION = 'us-east-1'
KEYPAIR_NAME = 'key_name'
INSTANCE_USER = 'ubuntu'

# Path to your EC2 key.
PATH_TO_KEY = 'keys/ec2key.pem'

# Looks for an `id_rsa.pub` and `id_rsa` in this directory,
# for accessing the Github repository.
PATH_TO_DEPLOY_KEYS = 'keys'

# Use a base Ubuntu 13.04 64bit us-east-1 EBS-backed image.
# For more, see:
# https://cloud-images.ubuntu.com/locator/ec2/
# Choose according to your region!
#BASE_AMI_ID = ami-a73371ce #instance-store
BASE_AMI_ID = 'ami-7d317314'
WORKER_AMI_ID = 'ami-7d317314'

# This will update itself when a new master instance is created.
MASTER_PUBLIC_DNS = 'localhost'

# Database port, which will be opened on the database instance.
# This is the Postgres default.
DB_PORT = 5432

MAIL_TARGETS = 'ftzeng@gmail.com'
