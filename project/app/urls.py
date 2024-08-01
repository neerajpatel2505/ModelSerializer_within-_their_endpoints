from django.urls import path
from .views import *

urlpatterns = [
    path('userList/',userList,name='userList'),
    path('userDetails/<int:pk>/',userDetails,name='userDetails')
]