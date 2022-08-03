from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import userList,userLogin,userRegister


urlpatterns = [
    path('token/obtain', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('register', userRegister.as_view()),
    path('login', userLogin.as_view()),
    path('users', userList.as_view()),
]
