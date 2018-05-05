import boto3
import botocore
from datetime import datetime, timezone
import socket
import pickle

s3 = boto3.resource('s3')
BUCKET = 'jagabucket3'
KEY = 'data.txt'  # file to be accessed
email = 'jsarava@ncsu.edu'


ob = s3.Object(BUCKET, KEY)
last_mod = ob.last_modified
start_time = datetime.now(timezone.utc)

try:
    s3.Bucket(BUCKET).download_file(KEY, KEY)
    print("downloaded")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

end_time = datetime.now(timezone.utc)
print("start time: " + str(start_time))
print("end time: " + str(end_time))
print("difference: " + str(end_time - start_time))

t1 = datetime.now(timezone.utc)

print("last mod time:", last_mod)
print("last accessed:", t1)
print("last acc - last modi ", str(t1 - last_mod))

y = []
y.append(BUCKET)
y.append(KEY)
y.append(last_mod)
y.append(t1)
y.append(email)

print(y)
data = pickle.dumps(y)

s = socket.socket()
print("Socket successfully created")
port = 12345
s.connect(('127.0.0.1', port))
print("socket binded to %s" % (port))
s.send(data)
print("socket is listening")
s.close()