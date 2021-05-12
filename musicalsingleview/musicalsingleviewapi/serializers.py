from django.db.models import fields
from rest_framework import serializers

from .models import Musicalwork

class MusicalworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musicalwork
        fields = '__all__'