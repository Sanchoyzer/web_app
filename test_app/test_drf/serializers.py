from rest_framework import serializers

from .models import PhoneBook


class PhoneBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneBook
        fields = ('name', 'phone')
