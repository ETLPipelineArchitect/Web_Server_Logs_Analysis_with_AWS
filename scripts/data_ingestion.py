import boto3

# Function to upload log files to S3

def upload_logs_to_s3(bucket_name, file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket_name, object_name)
    print(f'Uploaded {file_name} to {bucket_name}/{object_name}')

# Example of usage
# upload_logs_to_s3('your-bucket-name', 'path/to/log_file.log')
