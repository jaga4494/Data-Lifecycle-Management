import boto3
import socket
import pickle

s3 = boto3.resource('s3')
BUCKET = 'jagabucket1'
KEY = 'key1'  # file to be uploaded
email = 'jsarava@ncsu.edu'

# Upload a new file or modifying and uploading the same file--------------
data = open(KEY, 'rb')
s3.Bucket(BUCKET).put_object(Key=KEY, Body=data)

ob = s3.Object(BUCKET, KEY)
last_mod = ob.last_modified

print("last mod time:", last_mod)

y = []
y.append(BUCKET)
y.append(KEY)
y.append(last_mod)
y.append(last_mod) # last accessed is same as last modified is new object is uploaded
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
