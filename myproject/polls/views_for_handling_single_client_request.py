from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from polls.models import User, Bucket
import boto3
from datetime import datetime, timezone, timedelta
import json
import botocore
import socket
import pickle
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
import matplotlib.pyplot as plt; plt.rcdefaults()
from pylab import figure, axes, pie, title, show

# ex: /polls/objdetails
def displayObjectdetails(request):
    """Display present object entry details from model Bucket"""
    obj_list = Bucket.objects.all()
    context = {'obj_list': obj_list}
    return render(request, 'polls/objdetails.html', context)
s3 = boto3.resource('s3')
s3client = boto3.client('s3')
HOST =''
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
cycle_count = 5
cycle_time = 5

# Normal distribution Graph
def plot_normal_graph(start, end, count_list):
    """Plot graph"""
    xtime = []
    xstart = start
    delta = timedelta(seconds=cycle_time)
    t = []
    for i in range(0, len(count_list)):
        t.append(start)
        start += delta
    print(t)
    # y_pos = np.arange(len(count_list))
    print("count list: ", count_list)
    # plt.bar(y_pos, count_list, align='center')
    plt.hist(count_list)
    plt.xlabel("Over cycles")
    plt.ylabel("Request Count")
    # plt.show()
    plt.savefig('foo.png', bbox_inches='tight')


# ex: /polls/newobject
def newobject(request):
    """Run server to accept client requests"""
    msg = "Error occurred try again!!"
    try:
        c, addr = s.accept()
        cycle_start_time = datetime.now(timezone.utc) + timedelta(days=1)
        cycle_end_time = cycle_start_time + timedelta(days=4)
        a = pickle.loads(c.recv(1024))
        print(a[0])
        msg = " program started\r\n"
        obj_count = Bucket.objects.filter(bucket=a[0], object=a[1]).count()
        if obj_count != 0:
            # If entry is already present
            buc_entry = Bucket.objects.get(bucket=a[0], object=a[1])
            buc_entry.count = buc_entry.count + 1

            # to handle GET and put request for existing object
            msg += "existing last modi: " + str(buc_entry.last_modified) + "client passed last mod: " + str(a[2])
            if not str(buc_entry.last_modified) == str(a[2]):
                buc_entry.last_modified = a[2]
                msg += "last modi changed for PUT request"
            else:
                msg += "last modi unchanged for GET request"
            buc_entry.last_accessed = a[3]
            msg += "Bucket: " + str(a[0]) + " Object: " + str(a[1]) + " accessed"
            buc_entry.cycle['frequency'].append(calculate_frequency(buc_entry, cycle_start_time, cycle_end_time, msg))
            buc_entry.cycle['start_time'].append(str(cycle_start_time))
            buc_entry.cycle['end_time'].append(str(cycle_end_time))
            buc_entry.save()
        else:
            # If adding new entry and creation date is same as modified date
            freq =[]
            freq.append(round(1 / (cycle_end_time - a[2]).days, 2))
            start_time=[]
            start_time.append(str(cycle_start_time))
            end_time=[]
            end_time.append(str(cycle_end_time))
            buc_entry = Bucket(email=str(a[4]), bucket=str(a[0]), object=str(a[1]), creation_date=str(a[2]),
                               last_modified=str(a[2]),
                               last_accessed=str(a[3]), count=1, cycle={'start_time': start_time, 'end_time': end_time, 'frequency':freq})

            msg += "New entry added: " + "User: " + str(a[4]) + "Bucket: " + str(a[0]) + " Object: " + str(a[1])

            buc_entry.save()
        s.close()
        msg += "after saving in db"
    except Exception as e:
        return HttpResponse("<h2>" + e + "</h2>")

    # After a cycle ends, make count of all entry to zero and calculate cumaulative frequency
    # set_count_zero()
    calculate_cumulative_frequency("")
    return HttpResponse("<h2>" + msg + "</h2>")


def calculate_cumulative_frequency(noise):
    """Calculate cumulative frequency at the end of each cycle"""
    entry_list = Bucket.objects.all()
    for entry in entry_list:
        freq_len = len(entry.cycle['frequency'])
        if not freq_len:
            freq_len = 1
        frequency = round(sum(entry.cycle['frequency']) / freq_len, 2)
        if not noise == "noise":
            entry.frequency = frequency
            entry.save()


def calculate_frequency(entry, cycle_start_time, cycle_end_time, msg):
    """Calculates frequency of a passed entry"""
    if entry.count == 0:
        frequency = 0.0
    else:
        msg += "\r\n" + "count: " + str(entry.count) + "start: " + str(cycle_start_time) + " end: " + str(
            cycle_end_time)
        if entry.creation_date is not None and entry.creation_date > cycle_start_time:
            msg += "creation: " + str(entry.creation_date)
            frequency = round(entry.count / (cycle_end_time - entry.creation_date).days, 2)
        else:
            frequency = round(entry.count / (cycle_end_time - cycle_start_time).days, 2)
    msg += " frequency: " + str(frequency) + "\r\n"
    print("\r\n" + msg + "\r\n")
    return frequency


def calculate_cumulative_frequency_each(entry):
    """Calculate cumulative frequency at the end of each cycle"""
    freq_len = len(entry.cycle['frequency'])
    if not freq_len:
        freq_len = 1
    frequency = round(sum(entry.cycle['frequency']) / freq_len, 2)
    return frequency


def prepare_for_noise():
    entry_list = Bucket.objects.all()
    for entry in entry_list:
        entry.count =0
        entry.cycle['frequency']=[]
        entry.cycle['start_time']=[]
        entry.cycle['end_time']=[]
        entry.save()


def set_count_zero():
    """Set count field to zero after each cycle"""
    Bucket.objects.all().update(count=0)


# ex: /polls/jsarava@ncsu.edu/<bucketname>/<objectname>/cycle
def display_object_cycle(request, user_email, bucket_name, object_name):
    """Display all previous cycles of a object"""
    obj = Bucket.objects.get(bucket=bucket_name, object=object_name)
    context ={'obj_cumulative_freq': obj.frequency, 'obj_start_time': obj.cycle['start_time'], 'obj_end_time': obj.cycle['end_time'], 'obj_frequency': obj.cycle['frequency']}
    return render(request, 'polls/display_object_cycle.html', context)


# ex: /polls/newuser
def newuser(request):
    """Add new user"""
    context = {}
    result = {}
    if request.POST.get('email'):
        result["name"] = request.POST.get('name')
        result["email"] = request.POST.get('email')
        result["accesskey"] = request.POST.get('accesskey')
        result["secretkey"] = request.POST.get('secretkey')
        new_user = User(name=result["name"], email=result["email"], accesskey=result["accesskey"],
                        secretkey=result["secretkey"])
        new_user.save()
        message = "User successfully added to the database!!"

    else:
        message = ''
        result = ''
    context = {'message': message, 'result': result}
    return render(request, 'polls/newuser.html', context)


# ex: /polls/
def index(request):
    """Home page of application"""
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'polls/index.html', context)


# ex: /polls/jsarava@ncsu.edu/<bucketname>/addlifecycle
def addlifecycle(request, user_email, bucket_name):
    """Add a lifecycle rule to a bucket"""
    result = {}
    context = {'email': user_email}
    newrule = {}
    newrule_json = {}
    if request.GET.get('rule'):

        result["rule"] = request.GET.get('rule')
        result["Storage_IA"] = request.GET.get('ia')
        result["Glacier"] = request.GET.get('glacier')
        result["Expire"] = request.GET.get('expire')

        if (int(result["Storage_IA"]) >= 30 and int(result["Glacier"]) >= int(result["Storage_IA"]) + 30
                and int(result["Expire"]) > int(result["Glacier"])):
            s3client = boto3.client('s3')
            print('inside lifecycle')
            newrule = s3client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={
                    'Rules': [
                        {
                            'Expiration': {
                                'Days': int(result["Expire"]),
                            },
                            'ID': str(result["rule"]),
                            'Filter': {
                                'Prefix': '',
                            },
                            'Status': 'Enabled',
                            'Transitions': [
                                {
                                    'Days': int(result["Storage_IA"]),
                                    'StorageClass': 'STANDARD_IA'
                                },
                                {
                                    'Days': int(result["Glacier"]),
                                    'StorageClass': 'GLACIER'
                                },
                            ],
                        },
                    ]
                }
            )

            newrule = json.dumps(newrule)
            newrule_json = json.loads(newrule)
            message = "Following rule has been successfully added to the bucket"
            context = {'result': result, 'message': message, 'email': user_email, 'httpcode': newrule_json}
        else:
            message = "Wrong values entered!!"
            context = {'result': result, 'message': message, 'email': user_email}
    return render(request, 'polls/addlifecycle.html', context)


# ex: /polls/jsarava@ncsu.edu
def about(request, user_email):
    user = get_object_or_404(User, pk=user_email)
    context = {'user': user}
    return render(request, 'polls/about.html', context)


# ex: /polls/jsarava@ncsu.edu/bucket
def bucket(request, user_email):
    """Display Bucket list and option to download and add lifecycle rule"""
    # newobject(request, user_email)
    user = get_object_or_404(User, pk=user_email)
    s3 = boto3.resource('s3', aws_access_key_id=user.accesskey, aws_secret_access_key=user.secretkey)
    bucketlist = s3.buckets.all()
    context = {'user': user, 'bucketlist': bucketlist}
    if request.GET.get('bucketname'):
        context['download_message'] = download(request, str(request.GET.get('bucketname')), user_email)
    return render(request, 'polls/bucket.html', context)


# ex: /polls/jsarava@ncsu.edu/bucket/<bucketname>
def object(request, user_email, bucket_name):
    """Display Object list"""
    response = "Objects present in bucket of user %s are %s."
    user = get_object_or_404(User, pk=user_email)
    s3 = boto3.resource('s3', aws_access_key_id=user.accesskey, aws_secret_access_key=user.secretkey)
    bucket = s3.Bucket(bucket_name)
    context = {'bucket': bucket, 'email': user_email}
    return render(request, 'polls/object.html', context)


# ex: /polls/jsarava@ncsu.edu/bucket/<bucketname>/download
def download(request, bucket_name, user_email):
    """Download whole bucket"""
    try:
        user = get_object_or_404(User, pk=user_email)
        s3 = boto3.resource('s3', aws_access_key_id=user.accesskey, aws_secret_access_key=user.secretkey)
        s3.meta.client.head_bucket(Bucket=bucket_name)
        bucket = s3.Bucket(bucket_name)
        if len(list(bucket.objects.all())) == 0:
            return "Bucket is empty!!"

        for obj in bucket.objects.all():
            s3.Bucket(bucket_name).download_file(obj.key, str(obj.key))
        return "The bucket is downloaded !!"
    except botocore.exceptions.ClientError:
        return "You do not have required permission to access this page or required object does not exist !!"



