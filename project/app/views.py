from django.shortcuts import render
# from django.contrib.auth.models import User
from .models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io
import json
from rest_framework.parsers import JSONParser

from django.http import HttpResponse,JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def userList(request): 
    if request.method =="GET":
        user = User.objects.all()
        serializer_data = UserSerializer(user,many=True)
        json_data = JSONRenderer().render(serializer_data.data)
        return HttpResponse(json_data,content_type = 'application/json')
    
    elif request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = UserSerializer(data = python_data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

@csrf_exempt
def userDetails(request,pk):
    if request.method=='GET':
        id = User.objects.filter(id=pk)
        if id:
            stu = User.objects.get(id=pk)
            serializer_data = UserSerializer(stu)
            print(serializer_data.data)
            json_data = JSONRenderer().render(serializer_data.data)
            return HttpResponse(json_data,content_type = 'application/json')
        else:
            res = {'msg': 'id not present in Database'}
            return JsonResponse(res)
    
    elif request.method == 'PUT':
        id = User.objects.get(id=pk)
        if id:
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            stu = User.objects.get(id=pk)
            serializer = UserSerializer(stu, data=python_data, partial = True)
            # serializer = UserSerializer(stu, data=python_data)
            if serializer.is_valid():
                serializer.save()
                res = {'msg':'Data Updated !!'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        else:
            res = {'msg': 'id not present in Database'}
            return JsonResponse(res)
    
    elif request.method == 'PATCH':
        id = User.objects.filter(id=pk)
        if id:
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            stu = User.objects.get(id=pk)
            serializer = UserSerializer(stu, data=python_data, partial = True)
            # serializer = UserSerializer(stu, data=python_data)
            if serializer.is_valid():
                serializer.save()
                res = {'msg':'Data Partially Updated !!'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        else:
            res = {'msg': 'id not present in Database'}
            return JsonResponse(res)

    elif request.method == 'DELETE':
        id = User.objects.get(id=pk)
        if id:
            stu = User.objects.get(id=pk)
            stu.delete()
            res = {'msg': 'Data Deleted!!'}
            return JsonResponse(res, safe=False)
        else:
            res = {'msg': 'id not present in Database'}
            return JsonResponse(res)