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
from .models import Goods
from  .models import Car
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
        return JsonResponse(goods,safe=False)

@csrf_exempt
def add(request):
        data = json.loads(request.body)
        good_id = data.get('good_id')
        good_from = data.get('good_from')
        good_title = data.get('good_title')
        good_link = data.get('good_link')
        good_img = data.get('good_id')
        account = data.get('account')
        good_price=data.get('good_price')
        print(good_price)
        condition = Goods.objects.filter(good_id=good_id).exists()
        if condition:
                user = User.objects.filter(username=account).first()
                good = Goods.objects.filter(good_id=good_id).first()
                good_pid = good.price_queue_id
                if good_pid==0:
                        good.good_price0=good_price
                        good.price_queue_id=1
                elif good_pid==1:
                        good.good_price1=good_price
                        good.price_queue_id=2
                elif good_pid==2:
                        good.good_price2=good_price
                        good.price_queue_id=3
                elif good_pid==3:
                        good.good_price3=good_price
                        good.price_queue_id=4
                else:
                        good.good_price4=good_price
                        good.price_queue_id=0
                in_car =  Car.objects.filter(good_id=good.id).filter(user_id=user.id).exists()
                good.save()
                good = Goods.objects.filter(good_id=good_id).first()
                if in_car:
                        return HttpResponse("重复添加购物车")
                else:
                        try:
                                new_car = Car(good_id=good,user_id=user)
                                new_car.save()
                                return HttpResponse("success")
                        except IntegrityError as e2:
                                return HttpResponse("出错了请重试")
        else:
                try:
                        new_good=Goods(good_id=good_id,good_from=good_from,
                                       good_title=good_title,good_link=good_link,
                                       good_img=good_img,good_price0=good_price,
                                       good_price1=good_price,good_price2=good_price,
                                       good_price3=good_price,good_price4=good_price)
                        new_good.save()
                        user = User.objects.filter(username=account).first()
                        good = Goods.objects.filter(good_id=good_id).first()
                        new_car = Car(good_id=good, user_id=user)
                        new_car.save()
                        return HttpResponse("success")
                except IntegrityError as e2:
                        return HttpResponse("出错了请重试")

