from django.contrib import auth
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import response, status
from SII_API.models import Sii_Api, User
from SII_API.serializers import ApiSerializer
from rest_framework.decorators import api_view
import jwt
from Token.Auth import *

# encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")


@api_view(['GET', 'POST'])
def sensors(request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()
        titre = request.GET.get('type', None)
        if titre is not None:
            data = data.filter(contien=titre)
        data_serializer = ApiSerializer(data, many=True)

        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def new_data(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serial = ApiSerializer(data=data)
        if serial.is_valid():
            serial.save()
            return JsonResponse(serial.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    pass


@api_view(['GET', 'POST'])
def sensors_id(request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        mongoId = request.GET.get('idApp', None)
        #if mongoId is not None:
        data = data.filter(idApp=66666).order_by("-date")

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def alerts(request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        alerte = request.GET.get('alerte', None)
        #if alerte is not None:
        data = data.filter(alerte="False").order_by("-date")

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def sensors_id_alerts(request):
    pass


@api_view(['POST'])
def authenticate(request):
    auth.authenticate(request)


@api_view(['POST'])
def login(request):
    loginData = None
    if not request.data:
        return response.Response({'Error': "Please provide username/password"}, status="400")

    username = request.data['username']
    password = request.data['password']
    try:
        # loginData = User.objects.all()
        loginData = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        print(loginData)
        return response.Response({'Error': "Invalid username/password"}, status="400")
    if loginData:

        payload = {
            'userid': loginData.id,
            # 'email': loginData.email,
        }
        jwt_token = {'token': jwt.encode(payload, "SECRET_KEY", algorithm="HS256")}

        return HttpResponse(
            json.dumps(jwt_token),
            status=200,
            content_type="application/json"
        )

    else:
        print(loginData)
        return response.Response(
            json.dumps({'Error': "Invalid credentials"}),
            status=400,
            content_type="application/json"
        )
