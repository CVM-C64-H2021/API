from rest_framework import status, exceptions, response
from django.http.response import HttpResponse, JsonResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.contrib.auth import get_user_model
from SII_API.models import User
import jwt
import json


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        print("this is the token:"+auth[1])
        if not auth or auth[0].lower() != b'token':
            #return None
            return response.Response(
            json.dumps({msg}),
            status=400,
            content_type="application/json"
        )

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            #raise exceptions.AuthenticationFailed(msg)
            return response.Response(
            json.dumps({msg}),
            status=400,
            content_type="application/json"
        )
        elif len(auth) > 2:
            msg = 'Invalid token header'
            #raise exceptions.AuthenticationFailed(msg)
            return response.Response(
            json.dumps({msg}),
            status=400,
            content_type="application/json"
        )

        try:
            token = auth[1]
            if token=="null":
                msg = 'Null token not allowed'
                #raise exceptions.AuthenticationFailed(msg)
                return response.Response(
            json.dumps({msg}),
            status=400,
            content_type="application/json"
        )
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            #raise exceptions.AuthenticationFailed(msg)
            return response.Response(
            json.dumps({msg}),
            status=400,
            content_type="application/json"
        )

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        payload = jwt.decode(token, "SECRET_KEY")
        userid = payload['userid']
        msg = {'Error': "Token mismatch",'status' :"401"}
        try:

            user = User.objects.get(
                userid=userid,
                is_active=True
            )

            if not user.token['token'] == token:
                raise exceptions.AuthenticationFailed(msg)

        except jwt.DecodeError or jwt.InvalidTokenError:
            return json.dumps.Response(json.dumps({'Error': "Token is invalid"}), status="403",content_type="application/json")
        except User.DoesNotExist:
            return  json.dumps.Response(json.dumps({'Error': "Token is invalid"}), status="500",content_type="application/json")

        #return (user, token)
        return response.Response(
            json.dumps({user+token}),
            status=400,
            content_type="application/json"
        )

    def authenticate_header(self, request):
        #return 'Token'
        return response.Response(
            json.dumps({user+token}),
            status=400,
            content_type="application/json"
        )