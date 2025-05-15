import boto3
import io
from PIL import Image

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

def check_face_exists(image_binary):
    # Send image to Rekognition and check if face exists in collection
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
        return True, face_id, confidence
    else:
        print("No matching face found.")
        return False, None, None

def main():
    image_binary = preprocess_image("karina-test.jpg")
    check_face_exists(image_binary)

if __name__ == "__main__":
    main()