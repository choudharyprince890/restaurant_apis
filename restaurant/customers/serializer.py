
from accounts.models import User,Restaurant_owner
from rest_framework import serializers
from .models import Customer_detail





class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
class RestaurantOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_owner
        fields = ('id', 'user')
class customerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_detail
        fields = '__all__'


class customermListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_detail
        fields = '__all__'


