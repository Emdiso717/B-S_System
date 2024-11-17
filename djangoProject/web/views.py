from audioop import error

from django.contrib.auth import authenticate
from django.contrib.messages import success
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
import web.SN_spider as SN
import web.A_spider as A

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
def searchJD(request):
        data=json.load(request)
        search_data=data.get('search')
        goods = JD.search_goods(search_data)
        return JsonResponse(goods,safe=False)

@csrf_exempt
def searchSN(request):
        data=json.load(request)
        search_data=data.get('search')
        goods = SN.search_good(search_data)
        return JsonResponse(goods,safe=False)

@csrf_exempt
def searchA(request):
        data=json.load(request)
        search_data=data.get('search')
        goods = A.search_good(search_data)
        return JsonResponse(goods,safe=False)

@csrf_exempt
def add(request):
        data = json.loads(request.body)
        good_id = data.get('good_id')
        good_from = data.get('good_from')
        good_title = data.get('good_title')
        good_link = data.get('good_link')
        good_img = data.get('good_img')
        account = data.get('account')
        good_price=data.get('good_price')
        # print(good_price)
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
                                return HttpResponse("出错了请重试1")
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

@csrf_exempt
def search_car(request):
        data = json.load(request)
        account = data.get('account')
        user = User.objects.filter(username=account).first()
        cars = Car.objects.filter(user_id=user)
        goods_all = []
        for car in cars:
                goods={}
                # print(car.good_id.id)
                good = Goods.objects.filter(id = car.good_id.id).first()
                goods['id']=good.id
                if good.good_from=='JD':
                        goods['from']='京东'
                elif good.good_from=='SN':
                        goods['from'] = '苏宁'
                else:
                        goods['from'] = '唯品会'
                goods['title'] = good.good_title
                goods['link'] = good.good_link
                goods['img'] = good.good_img
                price_id = good.price_queue_id
                if price_id==0:
                        goods['price'] = good.good_price4
                        goods['price1'] = good.good_price0
                        goods['price2'] = good.good_price1
                        goods['price3'] = good.good_price2
                        goods['price4'] = good.good_price3
                elif price_id==1:
                        goods['price'] = good.good_price0
                        goods['price1'] = good.good_price1
                        goods['price2'] = good.good_price2
                        goods['price3'] = good.good_price3
                        goods['price4'] = good.good_price4
                elif price_id==2:
                        goods['price'] = good.good_price1
                        goods['price1'] = good.good_price2
                        goods['price2'] = good.good_price3
                        goods['price3'] = good.good_price4
                        goods['price4'] = good.good_price0
                elif price_id==3:
                        goods['price'] = good.good_price2
                        goods['price1'] = good.good_price3
                        goods['price2'] = good.good_price4
                        goods['price3'] = good.good_price0
                        goods['price4'] = good.good_price1
                else:
                        goods['price'] = good.good_price3
                        goods['price1'] = good.good_price4
                        goods['price2'] = good.good_price0
                        goods['price3'] = good.good_price1
                        goods['price4'] = good.good_price2
                goods_all.append(goods)
        # print(goods_all)
        return JsonResponse(goods_all, safe=False)

@csrf_exempt
def car_delete(request):
        data = json.loads(request.body)
        account=data.get('account')
        good_id=data.get('good_id')
        user = User.objects.filter(username=account).first()
        good = Goods.objects.filter(id = good_id).first()
        car = Car.objects.filter(user_id=user).filter(good_id=good).first()
        try:
                car.delete()
                return HttpResponse("success")
        except IntegrityError as e2:
                return HttpResponse("错误")

