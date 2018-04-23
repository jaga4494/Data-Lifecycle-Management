from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    # ex: /polls/newobject
    path('newobject/', views.newobject, name='newobject'),

    # ex: /polls/objdetails
    path('objdetails/', views.displayObjectdetails, name='displayObjectdetails'),

    # ex: /polls/newuser
    path('newuser/', views.newuser, name='newuser'),

    # ex: /polls/jsarava@ncsu.edu
    path('<str:user_email>/', views.about, name='about'),

    # ex: /polls/jsarava@ncsu.edu/bucket
    path('<str:user_email>/bucket/', views.bucket, name='bucket'),

    # ex: /polls/jsarava@ncsu.edu/bucket/<bucketname>
    path('<str:user_email>/bucket/<str:bucket_name>/', views.object, name='object'),

    # ex: /polls/jsarava@ncsu.edu/bucket/<bucketname>/download
    path('<str:user_email>/bucket/<str:bucket_name>/download/', views.download, name='download'),

    # ex: /polls/jsarava@ncsu.edu/<bucketname>/addlifecycle
    path('<str:user_email>/<str:bucket_name>/addlifecycle/', views.addlifecycle, name='addlifecycle'),
]
