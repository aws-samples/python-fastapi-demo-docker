import time
import psycopg2
import logging
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import boto3
from botocore.exceptions import ClientError
import json

def wait_for_db(db_url, max_retries=10, wait_time=1):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    result = urlparse(db_url)
    dbname = result.path[1:]
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    retries = 0

    logger.info(f"Trying to connect to {host}:{port} as {user}...")

    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            conn.close()
            logger.info("Connection successful!")
            return
        except Exception as e:
            logger.warning(f"Postgres is not ready yet. Waiting... {str(e)}")
            time.sleep(wait_time)
            retries += 1

    logger.error("Max retries reached. Unable to connect to the database.")

# Retrieves secret by name from AWS Secrets Manager
def get_secret(secret_name):

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary']

secret_data = get_secret('eksdevworkshop-db-url')

# Parse the json string in secret_data and extract connectionstring
DATABASE_URL = json.loads(secret_data)['connectionstring']

print("Database URL:", DATABASE_URL)

wait_for_db(DATABASE_URL)

engine = create_engine(DATABASE_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)