from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import MusicalworkSerializer
from .models import Musicalwork

# Create your views here.

class MusicalworkViewSet(viewsets.ModelViewSet):
    queryset = Musicalwork.objects.all().distinct('iswc')
    serializer_class = MusicalworkSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['=iswc']
