from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User
from django.template import loader
import boto3
import json
import botocore
from django.http import HttpResponseRedirect
# Create your views here.

# ex: /polls/newuser
def newuser(request):
    context={}
    result={}
    if request.POST.get('email'):

        result["name"]=request.POST.get('name')
        result["email"]=request.POST.get('email')
        result["accesskey"]=request.POST.get('accesskey')
        result["secretkey"]=request.POST.get('secretkey')
        new_user=User(name=result["name"], email=result["email"], accesskey=result["accesskey"], secretkey=result["secretkey"])

        new_user.save()
        message="User successfully added to the database!!"

    else:
        message="not posted"
        result=''
    context={'message': message, 'result':result}
    return render(request,'polls/newuser.html',context)

# ex: /polls/
def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request,'polls/index.html',context)

# ex: /polls/jsarava@ncsu.edu/<bucketname>/addlifecycle
def addlifecycle(request, user_email, bucket_name):
    result={}
    context={'email': user_email}
    newrule={}
    newrule_json={}
    if request.GET.get('rule'):

        result["rule"]=request.GET.get('rule')
        result["Storage_IA"]=request.GET.get('ia')
        result["Glacier"]=request.GET.get('glacier')
        result["Expire"]=request.GET.get('expire')


        #error for Wrong values


        if(int(result["Storage_IA"])>=30 and int(result["Glacier"]) >= int(result["Storage_IA"]) + 30
        and int(result["Expire"]) > int(result["Glacier"])):
            s3client=boto3.client('s3')
            print('inside lifecycle')
            newrule= s3client.put_bucket_lifecycle_configuration(
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
            print('--------------------------------------------------------------------')
            print("type of new rule:", type(newrule))
            newrule= json.dumps(newrule)
            print("type of new rule after dumps:", type(newrule))
            newrule_json= json.loads(newrule)
            print("type of new rule_json:", type(newrule_json))

            message = "Following rule has been successfully added to the bucket"
            context = {'result': result, 'message': message, 'email': user_email, 'httpcode': newrule_json}  # user email is also passed
        else:
            message = "Wrong values entered!!"
            context={'result':result, 'message':message, 'email': user_email } # user email is also passed
    return render(request, 'polls/addlifecycle.html', context)

# ex: /polls/jsarava@ncsu.edu
def about(request, user_email):
    user = get_object_or_404(User, pk=user_email)
    context={'user':user}
    return render(request, 'polls/about.html', context)

# ex: /polls/jsarava@ncsu.edu/bucket
def bucket(request, user_email):
    user = get_object_or_404(User, pk=user_email)
    s3 = boto3.resource('s3', aws_access_key_id=user.accesskey, aws_secret_access_key=user.secretkey)
    bucketlist = s3.buckets.all()
    return render(request, 'polls/bucket.html', {'user':user, 'bucketlist': bucketlist,})

# ex: /polls/jsarava@ncsu.edu/bucket/<bucketname>
def object(request, user_email, bucket_name):
    response = "Objects present in bucket of user %s are %s."
    user = get_object_or_404(User, pk=user_email)
    s3 = boto3.resource('s3', aws_access_key_id=user.accesskey, aws_secret_access_key=user.secretkey)
    bucket = s3.Bucket(bucket_name)
    context ={'bucket':bucket}
    return render(request, 'polls/object.html', context)
