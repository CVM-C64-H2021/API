import json
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from SII_API.models import Sii_Api
from SII_API.serializers import ApiSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def sensors (request):
    # data = Sii_Api.objects.all()

    # data_serializer = ApiSerializer(data)
    with open('SII_API/testJSON.json') as json_file:
        data_test = json.load(json_file)
        data_dict = json.dumps(data_test)
    return HttpResponse(data_dict)

    # return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def new_data (request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serial = ApiSerializer(data=data)
        if serial.is_valid():
            serial.save()
            return JsonResponse(serial.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serial.errors,status=status.HTTP_400_BAD_REQUEST)

    pass

@api_view(['GET', 'POST'])
def sensors_id (request):
    pass

@api_view(['GET', 'POST'])
def alerts (request):
    pass

@api_view(['GET', 'POST'])
def sensors_id_alerts (request):
    pass

@api_view(['POST'])
def authenticate (request):
    pass