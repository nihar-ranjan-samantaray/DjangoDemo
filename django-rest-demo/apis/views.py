from asyncio.log import logger
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.decorators import api_view, schema, permission_classes
from django.conf import settings
import pytz
from pytz import timezone
import applogger
import json, re, csv
import datetime as dt
from datetime import date
tz = timezone('US/Pacific')
# import pandas as pd
# from sqlalchemy import create_engine

# import logging
# logger = logging.getLogger()

from .serializers import *
from .models import *

@api_view(['GET'])
@permission_classes((AllowAny,))  
def home(self):
    return Response({"status":"Success","message":"Home Page of Thbred Project"})


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'status': 1,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                # 'user': serializer.data
            }

            return Response(response, status=status_code)

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            now = dt.datetime.now()
            new_time = now + token_lifetime
            expire_in = str(new_time.strftime("%y-%m-%d %I:%M:%S"))
            response = {
                'status': 1,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'token': serializer.data['access'],
                'refresh_token': serializer.data['refresh'],
                'expire_in': expire_in,
                # 'authenticatedUser': {
                #     'username': serializer.data['username'],
                #     'role': serializer.data['role']
                # }
            }

            return Response(response, status=status_code)

class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'status': 0,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'status': 1,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

class MultiTableFetch(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            data = TableA.objects.prefetch_related('tableb_set', 'tablec_set').filter(id=1)
            for elements in data: 
                print(elements.field1)
                for det in elements.tableb_set.all():
                    print(det.field1)                    
                    print(det.field2)
                for det in elements.tablec_set.all():
                    print(det.field1)
                    print(det.field2)   
            logger.info("All Table Information Fetched Successfully")    
            return Response({"status":"success","message":"All Table Information Fetched Successfully"}, status=status.HTTP_200_OK)
        except:
            logger.exception("All Table Information Could Not be Fetched")
            return Response({"status":"fail","message":"All Table Information Could Not be Fetched"}, status=status.HTTP_400_BAD_REQUEST)

class UserLogOutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            '''
            refresh_token = self.request.data.get('refresh_token')
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response({"status": "OK, goodbye"})
            if self.request.data.get('all'):
            '''
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status":"success" ,"message":"User logged Out Successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except:
            logger.exception("Logout Failed")
            return Response({"status":"fail","message":"Logout Failed"}, status=status.HTTP_400_BAD_REQUEST)

