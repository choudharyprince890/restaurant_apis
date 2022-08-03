from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import UserRegisterSerializer, customerDetailSerializer, RestaurantOwnerSerializer, customermListSerializer
from accounts.models import Restaurant_owner,User
from accounts.serializer import UserListSerializer
from . models import Customer_detail

# Create your views here.


class customerDetails(generics.GenericAPIView):
    customer_detail_serializer = customerDetailSerializer
    res_serializer = RestaurantOwnerSerializer
    permission_classes = (IsAuthenticated, )
    def post(self,request):
        print("user pk",request.user.pk) 
        res = Restaurant_owner.objects.get(user=request.user.pk)
        print("restaurant pk",Restaurant_owner.pk)
        user_register = UserRegisterSerializer(data=request.data)
        print('ok1',user_register)
        if user_register.is_valid():
            print('ok2') 
            user_register.save()
            user_register_id = user_register.data['id']
            print("user id", user_register_id)
            request.data._mutable = True
            request.data['user'] = user_register_id
            request.data['res'] =res.pk
            customer_detail = self.customer_detail_serializer(data=request.data)
            if customer_detail.is_valid():
                customer_detail.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code, 
                    'message': 'Detailes are filled!',
                }
                return Response(response, status=status_code)
            else:
                return Response(customer_detail.errors, status=status.HTTP_403_FORBIDDEN)        

        else:
            return Response(user_register.errors, status=status.HTTP_403_FORBIDDEN)        




class customerList(generics.ListAPIView):
    serializer_class = customermListSerializer
    serializer_userlist = UserListSerializer
    queryset = Customer_detail.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        print('ok')
        users = User.objects.all()
        print('this are users ',users)
        # print('serializer data....', serializer)
        if int(self.request.user.role) == 1:
            # print(self.request.user.role)
            return self.queryset