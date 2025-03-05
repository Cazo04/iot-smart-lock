from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib.parse

print('Loading function')

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

TABLE_NAME = "nt532_collection"
COLLECTION_ID = "nt532_collection"

# --------------- Helper Functions ------------------

def index_faces(bucket, key):
    response = rekognition.index_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        CollectionId=COLLECTION_ID
    )
    return response

def update_index(table_name, face_id, full_name):
    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            'RekognitionId': face_id,
            'FullName': full_name
        }
    )
    return response

# --------------- Main handler ------------------

def lambda_handler(event, context):
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        # Trigger Rekognition analyses face
        response = index_faces(bucket, key)

        # Check if any face detected
        if 'FaceRecords' in response and response['FaceRecords']:
            face_id = response['FaceRecords'][0]['Face']['FaceId']

            # Get metadata in S3
            ret = s3.head_object(Bucket=bucket, Key=key)
            person_full_name = ret['Metadata'].get('fullname', 'Unknown')

            # Update DynamoDB
            update_index(TABLE_NAME, face_id, person_full_name)

            print(f"Successfully indexed face {face_id} for {person_full_name}")

        else:
            print("No face detected in image:", key)

        return response

    except Exception as e:
        print(e)
        print(f"Error processing object {key} from bucket {bucket}.")
        raise e
