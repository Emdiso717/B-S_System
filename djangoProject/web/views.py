from audioop import error

from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import IntegrityError
import web.JD_spider as JD
@csrf_exempt
def login(request):
        data = json.loads(request.body)
        account = data.get('account')
        password = data.get('password')
        user = authenticate(username=account,password=password)
        if user is not None:
                return HttpResponse("success")
        else:
                return HttpResponse("用户名或密码错误")


@csrf_exempt
def register(request):
        data = json.loads(request.body)
        account = data.get('account')
        email=data.get('email')
        password = data.get('password')
        # 检查邮箱
        if  User.objects.filter(email=email).exists():
               return HttpResponse("错误：邮箱号重复使用")
        try:
                new_user=User(username=account,email=email)
                new_user.set_password(password)
                new_user.save()
                return HttpResponse("success")
        except IntegrityError as e2:
                return HttpResponse("错误：用户名重复使用")


@csrf_exempt
def search(request):
        data=json.load(request)
        search=data.get('search')
        goods = JD.search_goods(search)
        print(search)
        print(goods)
        return  HttpResponse("success")