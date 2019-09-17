from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer

from rest_framework.serializers import Serializer
from rest_framework.fields import IntegerField, CharField


class PersonParamSerializer(Serializer):
    limit = IntegerField(required=False)
    offset = IntegerField(required=False)
    name = CharField(required=False)


class PersonParams(object):
    def __init__(self, data):
        self.limit = data.get("limit",10)
        self.offset = data.get('offset', 0)
        self.name = data.get('name')




class PersonListView(APIView):

    def get(self, request, format=None):

        param_serializer = PersonParamSerializer(data=request.query_params)

        if not param_serializer.is_valid():
            return Response(data=param_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        params = PersonParams(param_serializer.data)

        queryset = Person.objects

        if params.name:
            queryset = queryset.filter(name__icontains=params.name)
        
        queryset = queryset.all()[params.offset:params.offset + params.limit]
    
        serializer = PersonSerializer(queryset, many=True)
        result_data = serializer.data
        result = {'result': result_data}

        return Response(result)
    
    def post(self, request, format=None):

        serializer = PersonSerializer(data=request.data)
        
        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PersonDetailView(APIView):

    def get(self, request, person_id=None):

        try:
            person = Person.objects.get(pk=person_id)

        except Person.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PersonSerializer(person)

        result = serializer.data
        
        return Response(result)
