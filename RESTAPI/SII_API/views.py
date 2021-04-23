from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from SII_API.models import Sii_Api
from SII_API.serializers import ApiSerializer
from rest_framework.decorators import api_view
# import jwt

# encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")

@api_view(['GET', 'POST'])
def sensors (request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()
        titre = request.GET.get('m_type', None)
        if titre is not None:
            data = data.filter(contien = titre)
        data_serializer = ApiSerializer(data, many=True)

        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET', 'POST']) #autostart sur un autre thread (checker pour django autostart)
def new_data (request):
    if request.method == 'POST':
        serial = ApiSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return JsonResponse(serial.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serial.errors,status=status.HTTP_400_BAD_REQUEST)
    pass

@api_view(['GET', 'POST'])
def sensors_id (request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        mongoId = request.GET.get('m_idApp', None)
        if mongoId is not None:
            data = data.filter(id__icontains=mongoId)

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)

@api_view(['GET', 'POST'])
def alerts (request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        alerte = request.GET.get('m_alerte', None)
        if alerte is not None:
            data = data.filter(m_alerte__icontains=alerte)

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def sensors_id_alerts (request):
    pass

@api_view(['POST'])
def authenticate (request):
    pass