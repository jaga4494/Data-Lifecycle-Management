#may need to export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
from datetime import datetime, date, time
import boto3
import botocore
# session = boto3.Session(profile_name='default')
client=boto3.client('s3')
# default_s3_client = session.client('s3')

s3 = boto3.resource(
    's3',
    # aws_access_key_id='AKIAJNOFGOPQQEQJDMQQ',
    # aws_secret_access_key='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'
    )
# Print out bucket names-----------------
for bucket in s3.buckets.all():
    print(bucket.name)

# Upload a new file--------------
# data = open('sampleimg1.png', 'rb')
# s3.Bucket('jagabucket1').put_object(Key='sampleimg1.png', Body=data)



# check if the bucket exists-------------
exists = True
try:
    s3.meta.client.head_bucket(Bucket='jagabucket1')
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False
if exists:
    print "Exists"
else:
    print "Not Exists"

# print the keys in a bucket------------------
# bucket = s3.Bucket('jagabucket1')
# for key in bucket.objects.all():
#     print key

# create a new bucket----------------
# s3.create_bucket(Bucket='jagabucket2')


# lifecycle configuration
# response = client.put_bucket_lifecycle_configuration(
#     Bucket='jagabucket2',
#     LifecycleConfiguration={
#         'Rules': [
#             {
#                 'Expiration': {
#                     'Date': datetime(2018,06,07,01,55,0,0,None),
#                     'Days': 60,
#                     'ExpiredObjectDeleteMarker': True|False
#                 },
#                 'ID': 'rule1',
#
#                 'Filter': {
#                     'Prefix': 'simple',
#
#                 },
#                 'Status': 'Enabled',
#                 'Transitions': [
#                     {
#                         'Date': datetime(2018,3,8,1,56,0,0,None),
#                         'Days': 60,
#                         'StorageClass': 'STANDARD_IA'
#                     },
#                 ],
#                 'NoncurrentVersionTransitions': [
#                     {
#                         'NoncurrentDays': 123,
#                         'StorageClass': 'STANDARD_IA'
#                     },
#                 ],
#                 # 'NoncurrentVersionExpiration': {
#                 #     'NoncurrentDays': 12
#                 # },
#                 # 'AbortIncompleteMultipartUpload': {
#                 #     'DaysAfterInitiation': 12
#                 # }
#
#             },
#         ]
#     }
# )
# print response
