import boto3
import io
from PIL import Image
import os
from slack_sdk import WebClient
from dotenv import load_dotenv, dotenv_values 

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='ap-southeast-1')
s3 = boto3.client('s3')

BUCKET_NAME = "nt532-bucket"
COLLECTION_ID = "nt532_collection"

def preprocess_image(image_path):
    # Convert image to binary format for Rekognition
    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream, format="JPEG")
    return stream.getvalue()

def check_face_exists(image_binary, slack_message_container):
    print("Searching for faces in the collection...")
    response = rekognition.search_faces_by_image(
        CollectionId=COLLECTION_ID,
        Image={'Bytes': image_binary},
        MaxFaces=1,
        FaceMatchThreshold=90
    )

    print("Rekognition Response:", response)

    if 'FaceMatches' in response and response['FaceMatches']:
        face_id = response['FaceMatches'][0]['Face']['FaceId']
        confidence = response['FaceMatches'][0]['Face']['Confidence']
        print(f"Face matched! FaceId: {face_id} with {confidence}% confidence.")
        slack_message_container['message'] = f"Unlocked successfully!!!"
        return True, face_id, confidence
    else:
        print("No matching face found.")
        slack_message_container['message'] = "Warning: Someone tried to unlock your locker!!!!"
        return False, None, None


def main():
    image_binary = preprocess_image("gdragon.jpg")
    
    slack_message = {'message': ''}
    check_face_exists(image_binary, slack_message)
    
    message_string = slack_message['message']

    ## Slack notifications
    load_dotenv("./.env")
    slack_token = os.getenv("SLACK_TOKEN") 
    
    client = WebClient(token=slack_token)
    client.chat_postMessage(
        channel="locker-notifications", 
        text=message_string, 
        username="Locker Buddy"
    )
    print("Message sent to Slack!")

if __name__ == "__main__":
    main()