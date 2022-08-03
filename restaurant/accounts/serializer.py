from .models import User, Restaurant_owner
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate





class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','password','role')

        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data): 
        user = User.objects.create(
            email=validated_data['email'],
            password = make_password(validated_data['password']),
            role=validated_data['role'],
        )
        return user


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_owner
        fields = '__all__' 


class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True) 
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass
    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        print(user,"user")
        if user is None:
            print('uphere')
            raise serializers.ValidationError("Invalid Login Credentials...")     
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            
            validation = {
                'access': access_token, 
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
                }
            return validation
        except User.DoesNotExist:
            print('downhere')
            raise serializers.ValidationError("Invalid Login Credentials")

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','role']

