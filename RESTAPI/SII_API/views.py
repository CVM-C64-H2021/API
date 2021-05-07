from django.contrib import auth
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import response, status
from SII_API.models import Sii_Api, User
from SII_API.serializers import ApiSerializer
from rest_framework.decorators import api_view
import jwt
from datetime import datetime, timedelta


@api_view(['GET'])
def sensors(request):
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 10)

    offset = int(offset)
    limit = min(int(limit),50)

    data = Sii_Api.objects.order_by("-date")[offset:limit]
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


@api_view(['GET'])
def alerts(request):
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 10)

    offset = int(offset)
    limit = min(int(limit),50)

    try:
        data = Sii_Api.objects.filter(alerte=True).order_by("-date")[offset:limit]
        data_serializer = ApiSerializer(data, many=True)
        return JsonResponse(data_serializer.data, safe=False)
    except Exception,e:
        return JsonResponse(e)

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


def authenticate(request):
    jwt_token = request.headers.get('authorization', None)

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, "SECRET_KEY", algorithm="HS256")
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return response.Response({'message': 'Token is invalid'}, status=400)

        id = payload['userid']
        try:

            user = User.objects.get(
                id=id,
            )

        except jwt.InvalidTokenError:
            return  response.Response({'Error': "Token is invalid"}, status="403",content_type="application/json")
        except user.DoesNotExist:
            return   response.Response({'Error': "Token mismatch"}, status="500",content_type="application/json")
        return response.Response({'User':user.username,"status":True},status="200")
    else:
        return response.Response({"message": "Token  does not exist"},status="400",contnt_type="application/json")


@api_view(['POST'])
def login(request):
    loginData = None
    if not request.data:
        return response.Response({'Error': "Please provide username/password"}, status="400")

    username = request.data['username']
    password = request.data['password']

    try:
        loginData = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
        return response.Response({'Error': "Invalid username/password"}, status="400")
    if loginData:

        payload = {
            'userid': loginData.id,
            'exp': datetime.utcnow() + timedelta(seconds=1000)
        }
        jwt_token = jwt.encode(payload, "SECRET_KEY", algorithm="HS256")
        print(jwt_token)
        return HttpResponse(
            json.dumps({'token': jwt_token.decode('utf-8')}),
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