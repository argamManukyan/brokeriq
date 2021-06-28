from django.core.exceptions import ValidationError
from django.http import request
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics, status,viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .pagination import CustomPagination
from .serializers import *
from .models import *
from core.serializers import *


class ClientsListAPI(generics.ListCreateAPIView):

    serializer_class = ClientListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Clients.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):

        serializer.save(broker_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClientCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        
        queryset = self.queryset
        query_data = self.request.query_params
        

        if query_data.get('draft'):
            print(query_data.get('draft')[0].upper() + query_data.get('draft')[1:].lower())
            draft = query_data.get('draft')[0].upper() + query_data.get('draft')[1:].lower()
            queryset = queryset.filter(draft=draft)
        if query_data.get('name') == 'ASC':
            queryset = queryset.order_by('name')
        if query_data.get('surname') == 'ASC':
            queryset = queryset.order_by('surname')
        if query_data.get('phone') == 'ASC':
            queryset = queryset.order_by('phone')
        if query_data.get('email') == 'ASC':
            queryset = queryset.order_by('email')
        if query_data.get('id') == 'ASC':
            queryset = queryset.order_by('id')
        if query_data.get('name') == 'DESC':
            queryset = queryset.order_by('-name')
        if query_data.get('surname') == 'DESC':
            queryset = queryset.order_by('-surname')
        if query_data.get('phone') == 'DESC':
            queryset = queryset.order_by('-phone')
        if query_data.get('id') == 'DESC':
            queryset = queryset.order_by('-id')
        if query_data.get('email') == 'DESC':
            queryset = queryset.order_by('-email')
        if query_data.get('from_date'):
            queryset = queryset.filter(created__gte=query_data.get('from_date'))
        if query_data.get('to_date') :
            queryset = queryset.filter(created__lte=query_data.get('to_date'))

        return queryset.filter(broker_id=self.request.user.id)

    
class ClientDetailViewAPI(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ClientDeleteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Clients.objects.all()
    lookup_field = 'pk'


    def get_queryset(self):

        query_data = self.request.query_params
        queryset = self.queryset
        if 'search' in query_data:
            queryset = Clients.objects.filter(Q(history__solution__icontains=query_data['search']) | Q(history__challenge_name__icontains=query_data['search']))

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientDetailSerializer
        if self.request.method in ['PATCH','PUT']:
            return ClientUpdateSerializer
        return super().get_serializer_class()
   

