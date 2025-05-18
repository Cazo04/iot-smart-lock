import cv2
import boto3
import io
import time
import os
from PIL import Image
from slack_sdk import WebClient
from dotenv import load_dotenv

rekognition = boto3.client('rekognition', region_name='ap-southeast-1')
COLLECTION_ID = "nt532_collection"

load_dotenv("./.env")
slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))

def process_face(frame):
    """Process detected face with AWS Rekognition and send Slack notification"""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    stream = io.BytesIO()
    pil_image.save(stream, format="JPEG")
    image_binary = stream.getvalue()
    
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': image_binary},
            MaxFaces=1,
            FaceMatchThreshold=90
        )
        
        if 'FaceMatches' in response and response['FaceMatches']:
            print(1)
            message = "Unlocked successfully!!!"
            return True, message
        else:
            print(0)
            message = "Warning: Someone tried to unlock your locker!!!!"
            return False, message
    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error processing face: {str(e)}"

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    startup_time = time.time()
    startup_delay = 10
    last_detection_time = 0
    cooldown_period = 30
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        display_frame = frame.copy()
        current_time = time.time()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        if current_time - startup_time < startup_delay:
            remaining = int(startup_delay - (current_time - startup_time))
            cv2.putText(display_frame, f"Starting in: {remaining}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        elif len(faces) > 0 and current_time - last_detection_time > cooldown_period:
            last_detection_time = current_time
            
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3]) if faces.size > 0 else None
            
            if largest_face is not None:
                x, y, w, h = largest_face
                face_img = frame[y:y+h, x:x+w]
                if face_img.size > 0:
                    recognized, message = process_face(frame)
                    
                    try:
                        slack_client.chat_postMessage(
                            channel="locker-notifications", 
                            text=message, 
                            username="Locker Buddy"
                        )
                    except Exception as e:
                        print(f"Slack error: {e}")
                    
                    status = "Access Granted" if recognized else "Access Denied"
                    color = (0, 255, 0) if recognized else (0, 0, 255)
                    cv2.putText(display_frame, status, (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        elif current_time - last_detection_time <= cooldown_period and last_detection_time > 0:
            remaining = int(cooldown_period - (current_time - last_detection_time))
            cv2.putText(display_frame, f"Cooldown: {remaining}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        
        cv2.imshow('Face Detection System', display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()