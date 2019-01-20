from django.db.models import Q
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import PhoneBookSerializer
from .models import PhoneBook

from builtins import len, staticmethod


class PhoneBookViewSet(viewsets.ModelViewSet):
    queryset = PhoneBook.objects.all()
    serializer_class = PhoneBookSerializer

    @action(detail=False, methods=['get'], name='Поиск по телефонному справочнику')
    def find(self, request):
        name = PhoneBookViewSet.get_valid_param(self.request, 'name')
        phone = PhoneBookViewSet.get_valid_param(self.request, 'phone')
        if name is None and phone is None:
            return Response(r'Введите параметры для поиска: имя и/или телефон',
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        query = PhoneBook.objects.all()
        if name is not None:
            query = query.filter(Q(name__icontains=name))
        if phone is not None:
            query = query.filter(Q(phone__icontains=phone))
        if query.count() == 0:
            return Response(r'По заданным параметрам ничего не найдено',
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data)

    @staticmethod
    def get_valid_param(request, param_name, min_len=3):
        param = request.query_params.get(param_name, None)
        if param is None or len(param) < min_len:
            return None
        else:
            return param


def index(request):
    return render(
        request,
        'test_drf/index.html',
        context={
            'search_url': '/drf/phoneBook/find/?name=',
            'add_url': '/drf/phoneBook/'
        },
    )

