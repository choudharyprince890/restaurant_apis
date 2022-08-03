from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status   
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST 
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.db import transaction
from .serializer import UserLoginSerializers,UserRegisterSerializer,User,UserListSerializer,RestaurantOwnerSerializer

class userRegister(generics.GenericAPIView):
    serializer_class = RestaurantOwnerSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        with transaction.atomic():
            user_serializer = UserRegisterSerializer(data=request.data)
            print("ok",user_serializer)
            if user_serializer.is_valid():
                user_serializer.save()
                print("only data",user_serializer.data)
                user = user_serializer.data['id']
                print("user_serializer id",user)
                request.data._mutable = True
                request.data['user'] = user
                serializer = self.serializer_class(data=request.data)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    serializer.save()
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'User successfully registered!',
                    }
                    return Response(response, status=status_code)
            else:
                return Response(user_serializer.errors)


class userLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializers
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }
            return Response(response, status=status_code)
        else:
            return Response(serializer.errors) 

class userList(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        print(request.user.role != 1,request.user.role)
        if int(request.user.role) != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'data': serializer.data
                }
            return Response(response, status=status.HTTP_200_OK)