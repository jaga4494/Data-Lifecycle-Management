import boto3
import botocore
from datetime import datetime, timezone
import socket
import pickle
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL

BUCKET = 'jagabucket1'
KEY = 'data1.txt'  # file to be downloaded
email = 'jsarava@ncsu.edu'
s3 = boto3.resource('s3')

HOST = ''
PORT = 50000  # The same port as used by the server
cycle_count = 10
min = 1
max = 30
factor = 0.11
noise_flag = 0  # If equal to 1, we add noise and send requests.


def add_noise(x):
    noise = int(factor * (np.random.randint(min, max, )))
    x -= noise
    return x


def send_request():
    try:
        for cycle in range(0, cycle_count):
            print("Cycle " + str(cycle + 1))

            x = np.random.randint(min, max)
            if noise_flag == 1:
                x = add_noise(x)
            count = 0
            data = []
            start_time = datetime.now(timezone.utc)
            for i in range(0, x):
                data = []
                ob = s3.Object(BUCKET, KEY)
                last_mod = ob.last_modified
                try:
                    s3.Bucket(BUCKET).download_file(KEY, 'downloaded.png')
                    print("downloaded")
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        print("The object does not exist.")
                    else:
                        raise
                cur_time = datetime.now(timezone.utc)
                data.append(BUCKET)
                data.append(KEY)
                data.append(last_mod)
                data.append(cur_time)
                data.append(email)

                if noise_flag == 1:
                    data.append("noise")  # [5]
                    data.append(min)  # [6]
                    data.append(max)  # [7]
                    data.append("random")
                else:
                    data.append("training")  # [5]

                print("sent data: " + str(data))
                y = pickle.dumps(data)
                s.send(y)
                rec = s.recv(2048).decode()
                print("received data: " + rec)
                if rec == "stop":
                    i = x
                count += 1
            s.send(str("next").encode())

            end_time = datetime.now(timezone.utc)
            print("total request: " + str(count))
            print("start time: " + str(start_time))
            print("end time: " + str(end_time))
            print("difference: " + str(end_time - start_time))
            print("--------------------------------------------")
    except Exception:
        signal(SIGPIPE, SIG_DFL)
        print("client closed")


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    send_request()
    s.close()
