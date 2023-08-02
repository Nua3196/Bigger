from django.shortcuts import render
from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer

#여러개
class NoticesAPI(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

#한개
class NoticeAPI(generics.RetrieveUpdateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = '_id'