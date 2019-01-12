from django.shortcuts import render

from .models import PhoneBook
from rest_framework import viewsets
from .serializers import PhoneBookSerializer


class PhoneBookViewSet(viewsets.ModelViewSet):
    queryset = PhoneBook.objects.all()
    serializer_class = PhoneBookSerializer
