from django.urls import path


from .views import *


urlpatterns = [
    path('details', customerDetails.as_view()),
    path('list', customerList.as_view()),
]