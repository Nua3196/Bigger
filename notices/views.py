from django.shortcuts import render
from rest_framework import generics
from .models import Notice, Update
from .serializers import NoticeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from background_task.models import Task
from getnotice import save_notices
from datetime import datetime

#여러개
class NoticesAPI(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

#한개
class NoticeAPI(generics.RetrieveUpdateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = '_id'

@api_view(['GET'])
def UpdateNoticesAPI(request):
    Notice.objects.all().delete()
    save_notices()
    Update.objects.create(how="hand")
    return Response("updated notices list")




    
