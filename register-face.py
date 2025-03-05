import boto3
import argparse

s3 = boto3.resource('s3')

s3_bucket_name = "nt532-bucket"

def upload_image(image_path, full_name):
    file_name = image_path.split('/')[-1]
    object = s3.Object(s3_bucket_name, 'index/' + file_name)
    
    with open(image_path, 'rb') as file:
        object.put(Body=file, Metadata={'FullName': full_name})

def main():
    parser = argparse.ArgumentParser(description="Upload an image to S3 with metadata")
    parser.add_argument("--path-to-image", required=True, help="Path to the image file")
    parser.add_argument("--name", required=True, help="Full name for metadata")
    args = parser.parse_args()
    upload_image(args.path_to_image, args.name)

if __name__ == "__main__":
    main()
