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
        serial = ApiSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return JsonResponse(serial.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    pass


@api_view(['GET'])
def sensors_id(request, id):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        mongoId = id
        offset = request.GET.get('offset', None)
        limit = request.GET.get('limit', None)
        if offset != None:
            offset = int(offset)
        if limit != None:
            limit = int(limit)
        if mongoId is not None:
            data = data.filter(idApp=mongoId).order_by("-date")[offset:limit]
        else:
            data = None

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET'])
def alerts(request):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        offset = request.GET.get('offset', None)
        limit = request.GET.get('limit', None)

        if offset != None:
            offset = int(offset)
        if limit != None:
            limit = int(limit)
        
        data = data.filter(alerte="True").order_by("-date")[offset:limit]

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)


@api_view(['GET'])
def sensors_id_alerts(request, id):
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        mongoId = id
        offset = request.GET.get('offset', None)
        limit = request.GET.get('limit', None)
        if offset != None:
            offset = int(offset)
        if limit != None:
            limit = int(limit)
        if mongoId is not None:
            data = data.filter(idApp=mongoId, alerte="True").order_by("-date")[offset:limit]
        else:
            data = None

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)


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
