from django.contrib import auth
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import response, status
from SII_API.models import Sii_Api, User
from SII_API.serializers import ApiSerializer
from rest_framework.decorators import api_view
import jwt
import json
from datetime import datetime, timedelta
import sys



@api_view(['GET'])
def sensors(request):
    # returnMsg = authenticate(request)
    # if returnMsg.status_code == 200:
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 10)

    offset = int(offset)
    limit = min(int(limit),50)

    data = Sii_Api.objects.order_by("-date")[offset:limit]
    data_serializer = ApiSerializer(data, many=True)
    return JsonResponse(data_serializer.data, safe=False)
    # else:
    #     return returnMsg

@api_view(['GET'])
def sensors_id(request, id):
    # returnMsg = authenticate(request)
    # if request.method == 'GET' and returnMsg.status_code == 200:
    if request.method == 'GET':
        data = Sii_Api.objects.all()

        mongoId = id
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)

        offset = int(offset)
        limit = min(int(limit),50)
        if mongoId is not None:
            data = data.filter(idApp=mongoId).order_by("-date")[offset:limit]
        else:
            data = None

        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)
    # else:
    #     return returnMsg


@api_view(['GET'])
def alerts(request):
    # returnMsg = authenticate(request)
    # if request.method == 'GET' and returnMsg.status_code == 200:
    if request.method == 'GET':
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)

        offset = int(offset)
        limit = min(int(limit),50)

<<<<<<< HEAD
    
    data = Sii_Api.objects.filter(type="image").order_by("-date")[offset:limit]
    data_serializer = ApiSerializer(data, many=True)
    return JsonResponse(data_serializer.data, safe=False)
=======
        data = Sii_Api.objects.filter(alerte=True).order_by("-date")[offset:limit]
        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)
    # else:
    #     return returnMsg
>>>>>>> 6af71f2f481c595b6e4471a4ca7040ab45e1fd93

@api_view(['GET'])
def sensors_id_alerts(request, id):
    # returnMsg = authenticate(request)
    # if request.method == 'GET' and returnMsg.status_code == 200:
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
    # else:
    #     return returnMsg


def authenticate(request):
    # jwt_token = request.headers.get('authorization', None)

    # if jwt_token:
    #     try:
    #         payload = jwt.decode(jwt_token, "SECRET_KEY", algorithm="HS256")
    #     except (jwt.DecodeError, jwt.ExpiredSignatureError):
    #         return response.Response({'message': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)

    #     id = payload['userid']
    #     try:

    #         user = User.objects.get(
    #             id=id,
    #         )

    #     except jwt.InvalidTokenError:
    #         return  response.Response({'Error': "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")
    #     except user.DoesNotExist:
    #         return   response.Response({'Error': "Token mismatch"}, status=status.HTTP_409_CONFLICT,content_type="application/json")
    #     return response.Response({'User':user.username,"status":True},status=status.HTTP_200_OK)
    # else:
    #     return response.Response({"message": "Token  does not exist"},status=status.HTTP_400_BAD_REQUEST,content_type="application/json")
    pass

@api_view(['POST'])
def login(request):
    loginData = None
    if not request.data:
        return response.Response({'Error': "Please provide username/password"}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data['username']
    password = request.data['password']

    try:
        loginData = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return response.Response({'Error': "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)
    if loginData:

        payload = {
            'userid': loginData.id,
            'exp': datetime.utcnow() + timedelta(seconds=1000)
        }
        jwt_token = jwt.encode(payload, "SECRET_KEY", algorithm="HS256")
        print(jwt_token)
        return HttpResponse(
            json.dumps({'token': jwt_token}),
            status=status.HTTP_200_OK,
            content_type="application/json"
        )
    else:
        print(loginData)
        return response.Response(
            json.dumps({'Error': "Invalid credentials"}),
            status=status.HTTP_400_BAD_REQUEST,
            content_type="application/json"
        )