import boto3
from botocore.exceptions import ClientError
from datetime import datetime

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    """
    Uploads an existing file to an S3 bucket.

    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the destination S3 bucket.
    :param object_name: The name of the object in S3. If not specified,
                        the file_path's base name is used.
    :return: True if file was uploaded successfully, else False.
    """
    # If S3 object_name is not specified, use the file name
    if object_name is None:
        # This takes the file name from a path like 'logs/app.log' -> 'app.log'
        import os
        object_name = os.path.basename(file_path)

    # Create an S3 client
    s3_client = boto3.client('s3')

    print(f"Uploading {file_path} to s3://{bucket_name}/{object_name}...")

    try:
        # The upload_file method is efficient for both small and large files
        s3_client.upload_file(file_path, bucket_name, object_name)
        print("✅ Upload Successful")
    except FileNotFoundError:
        print("Error: The file was not found.")
        return False
    except ClientError as e:
        print(f"Error: An AWS client error occurred: {e}")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return False
        
    return True
