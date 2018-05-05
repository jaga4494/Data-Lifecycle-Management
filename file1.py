# may need to export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
from datetime import datetime, date, time
import boto3
import botocore
import json
import time
from time import mktime
from datetime import datetime

s3client = boto3.client('s3')
# print(s3client.head_object(Bucket="jagabucket1", Key="4_666.png"))


# for glacier
# glacier = boto3.resource('glacier')
# vault = glacier.Vault('account_id','name')




# change the storage class of an object -- working
copy_source = {
    'Bucket': 'jagabucket1',
    'Key': 'abc.txt'
}

s3client.copy_from(
  copy_source, 'jagabucket1', 'abc.txt',
  ExtraArgs = {
    'StorageClass': 'GLACIER',
    'MetadataDirective': 'COPY'
  }
)
# change the storage class of an object -- working


# for other users----working
# s3 = boto3.resource('s3',
#          aws_access_key_id=AWS_ACCESS_KEY,
#          aws_secret_access_key=AWS_SECRET_ACCESS_KEY',
#          )

s3 = boto3.resource('s3')


# Print out bucket names-----------------
# for bucket in s3.buckets.all():
#     print(bucket.name)

# Upload a new file--------------
# data = open('sampleimg1.png', 'rb')
# s3.Bucket('jagabucket1').put_object(Key='sampleimg1.png', Body=data)

# Set bucket policy
# bucket_name = 'jagabucket3'
#
# key = s3.Bucket(bucket_name).get_key('data.txt')
# print("date: " + str(key.date))

# Create the bucket policy
# bucket_policy = {
#     'Version': '2012-10-17',
#     'Statement': [{
#         'Sid': 'AddPerm',
#         'Effect': 'Allow',
#         'Principal': '*',
#         'Action': ['s3:GetObject'],
#         'Resource': "arn:aws:s3:::%s/*" % bucket_name
#     }]
# }
#
# # Convert the policy to a JSON string
# bucket_policy = json.dumps(bucket_policy)
#
# # Set the new policy on the given bucket
# s3client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)




# check if the bucket exists-------------
# exists = True
# try:
#     s3.meta.client.head_bucket(Bucket='jagabucket1')
# except botocore.exceptions.ClientError as e:
#     # If a client error is thrown, then check that it was a 404 error.
#     # If it was a 404 error, then the bucket does not exist.
#     error_code = int(e.response['Error']['Code'])
#     if error_code == 404:
#         exists = Falses3 = boto3.connect_s3()
# if exists:
#     print "Exists"
# else:
#     print "Not Exists"

# print the objects in a bucket------------------
bucket = s3.Bucket('jagabucket1')

print(str(bucket.creation_date))
# for obj in bucket.objects.all():
#     print(obj.key,  obj.size, obj.last_modified, str(datetime.now()), str(obj.storage_class))

# ob = s3.Object('jagabucket3', 'data.txt')
# print(ob.created)

# key = bucket.get_key('data.txt')
# print(key)
# create a new bucket----------------
# s3.create_bucket(Bucket='jagabucket2')

# Call to S3 to retrieve the policy for the given bucket
# buc_exists=True
# try:
#     result = s3client.get_bucket_policy(Bucket='jagabucket1')
# except botocore.exceptions.ClientError as e:
#     error_message=e.response['Error']['Code']
#     buc_exists = False
# if buc_exists:
#     print(result)
# else:
#     print('Exception: ' + error_message)

# No use-----
# bucket = 'jagabucket1'
# bucket_lifecycle_configuration = s3.BucketLifecycleConfiguration(bucket)
# result= bucket_lifecycle_configuration.get_available_subresources()
# print result
# No use-----

# Download a file-------------- working
# KEY = '4_666.png' # file to be downloaded
# try:
#     s3.Bucket(bucket_name).download_file(KEY, 'my_local_4_666.png')
# except botocore.exceptions.ClientError as e:
#     if e.response['Error']['Code'] == "404":
#         print("The object does not exist.")
#     else:
#         raise
# Download a file-------------- working

# lifecycle configuration working---------------------

# bucket = 'jagabucket1'
# result= s3client.put_bucket_lifecycle_configuration(
#     Bucket=bucket,
#     LifecycleConfiguration={
#         'Rules': [
#             {
#                 'Expiration': {
#                     # 'Date': datetime(2018,04,04),
#                     'Days': 65,
#                     # 'ExpiredObjectDeleteMarker': True
#                 },
#                 'ID': 'rule1',
#                 # 'Prefix': '',
#                 'Filter': {
#                     'Prefix': '',
#                     # 'Tag': {
#                     #     'Key': 'tagkey1',
#                     #     'Value': 'tagvalue1'
#                     # },
#                     # 'And': {
#                     #     'Prefix': '/',
#                     #     'Tags': [
#                     #         {
#                     #             'Key': 'tagkey1',
#                     #             'Value': 'tagvalue1'
#                     #         },
#                     #     ]
#                     # }
#                 },
#                 'Status': 'Enabled',
#                 'Transitions': [
#                     {
#                         # 'Date': datetime(2018,04,04),
#                         'Days': 30,
#                         'StorageClass': 'STANDARD_IA'
#                     },
#                     {
#                         # 'Date': datetime(2018,04,04),
#                         'Days': 60,
#                         'StorageClass': 'GLACIER'
#                     },
#                 ],
#                 # 'NoncurrentVersionTransitions': [
#                 #     {
#                 #         'NoncurrentDays': 123,
#                 #         'StorageClass': 'STANDARD_IA'
#                 #     },
#                 # ],
#                 # 'NoncurrentVersionExpiration': {
#                 #     'NoncurrentDays': 30
#                 # },
#                 # 'AbortIncompleteMultipartUpload': {
#                 #     'DaysAfterInitiation': 30
#                 # }
#
#             },
#         ]
#     }
# )
# print(result)
# lifecycle configuration---------------------
