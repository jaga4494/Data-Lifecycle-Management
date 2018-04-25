from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from polls.models import User, Bucket
from django.template import loader
import boto3
import json
import botocore
import socket
import pickle
from django.utils.timezone import now

from django.http import HttpResponseRedirect

# ex: /polls/objdetails
def displayObjectdetails(request):
    """Home page of application"""
    obj_list = Bucket.objects.all()
    context = {'obj_list': obj_list}
    return render(request, 'polls/objdetails.html', context)

# ex: /polls/newobject
def newobject(request):
    msg = "Error occurred try again!!"
    try:
        s = socket.socket()
        port = 12345
        s.bind(('', port))
        s.listen(5)
        c, addr = s.accept()
        a = pickle.loads(c.recv(1024))
        print(a[0])
        obj_count = Bucket.objects.filter(bucket=a[0], object=a[1]).count()
        if obj_count != 0:
            buc_entry = Bucket.objects.get(bucket=a[0], object=a[1])
            # msg += str(obj_count) + " available entry "
            # msg += str(buc_entry.count) + " after get "
            buc_entry.count = buc_entry.count+1
            buc_entry.last_modified = a[2]
            buc_entry.last_accessed = a[3]
            # msg += "   after count"
            buc_entry.save()
            msg = "Bucket: " + str(a[0]) + " Object: " + str(a[1]) + " accessed"
        else:
            new_obj = Bucket(email=str(a[4]), bucket=str(a[0]), object=str(a[1]), last_modified=str(a[2]),
                             last_accessed=str(a[3]), count=1)
            new_obj.save()
            msg = "New entry added: " + "User: " + str(a[4]) + "Bucket: " + str(a[0]) + " Object: " + str(a[1])
        s.close()
        return HttpResponse("<h2>" + msg + "</h2>")
    except:
        return HttpResponse("<h2>" + msg + "</h2>")


# ex: /polls/newuser
def newuser(request):
    """Method to add new user"""
    context = {}
    result = {}
    if request.POST.get('email'):
        result["name"] = request.POST.get('name')
        result["email"] = request.POST.get('email')
        result["accesskey"] = request.POST.get('accesskey')
        result["secretkey"] = request.POST.get('secretkey')
        new_user = User(name=result["name"], email=result["email"], accesskey=result["accesskey"], secretkey=result["secretkey"])
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
    context = {'user': user, 'bucketlist': bucketlist }
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

