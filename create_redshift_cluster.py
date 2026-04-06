import boto3
import configparser
import time

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

KEY = config.get('AWS','KEY')
SECRET = config.get('AWS','SECRET')
SESSION_TOKEN = config.get('AWS','SESSION_TOKEN')
DWH_CLUSTER_IDENTIFIER = "sparkify-cluster-new"
DWH_DB = "dev"
DWH_DB_USER = "awsuser"
DWH_DB_PASSWORD = "Admin12345678"
DWH_PORT = 5439
DWH_NODE_TYPE = "ra3.4xlarge"
DWH_NUM_NODES = 2
ROLE_ARN = config.get("IAM_ROLE","ARN")

# CREATE CLIENT
redshift = boto3.client(
    'redshift',
    region_name='us-west-2',
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
    aws_session_token=SESSION_TOKEN
)

# CREATE CLUSTER
try:
    response = redshift.create_cluster(
        ClusterType='multi-node' if DWH_NUM_NODES>1 else 'single-node',
        NodeType=DWH_NODE_TYPE,
        NumberOfNodes=DWH_NUM_NODES,
        DBName=DWH_DB,
        ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
        MasterUsername=DWH_DB_USER,
        MasterUserPassword=DWH_DB_PASSWORD,
        IamRoles=[ROLE_ARN],
        PubliclyAccessible=True
    )
    print("Cluster creation started...")
except Exception as e:
    print("Error creating cluster:", e)

# CHECK CLUSTER STATUS
while True:
    try:
        response = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)
        status = response['Clusters'][0]['ClusterStatus']
        print(f"Cluster status: {status}")
        if status == 'available':
            print("Cluster is ready ✅")
            break
    except redshift.exceptions.ClusterNotFoundFault:
        print("Cluster not found yet, waiting...")
    time.sleep(30)