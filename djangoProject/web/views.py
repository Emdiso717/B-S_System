from audioop import error
from datetime import datetime
from time import sleep

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
from .check_price import check_price
from .check_price import send_emails
from .models import Goods
from  .models import Car
import web.SN_spider as SN
import web.A_spider as A
import re
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse


@csrf_exempt
def login(request):
        if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser('superqjz', 'admin@example.com', '12345678')
        data = json.loads(request.body)
        account = data.get('account')
        password = data.get('password')
        user = authenticate(username=account,password=password)
        if user is not None:
                payload = {
                        'account':account ,
                        'exp': datetime.utcnow() + timedelta(minutes=30)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return JsonResponse({'token': token})
        else:
                return HttpResponse("用户名或密码错误")


@csrf_exempt
def register(request):
        if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser('superqjz', 'admin@example.com', '12345678')
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
                goods['price'] = re.search(r"(\d+(\.\d{2})?)", goods['price']).group(1)
                goods['price'] = float(goods['price'])
                goods['price1'] = re.search(r"(\d+(\.\d{2})?)", goods['price1']).group(1)
                goods['price1'] = float(goods['price1'])
                goods['price2'] = re.search(r"(\d+(\.\d{2})?)", goods['price2']).group(1)
                goods['price2'] = float(goods['price2'])
                goods['price3'] = re.search(r"(\d+(\.\d{2})?)", goods['price3']).group(1)
                goods['price3'] = float(goods['price3'])
                goods['price4'] = re.search(r"(\d+(\.\d{2})?)", goods['price4']).group(1)
                goods['price4'] = float(goods['price4'])
                goods_all.append(goods)
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

@csrf_exempt
def get_A(request):
        src = A.get_src()
        print(src)
        return HttpResponse(src)
@csrf_exempt
def login_A(request):
        if A.login():
                return HttpResponse("success")

@csrf_exempt
def get_SN(request):
        src = SN.get_src()
        print(src)
        return HttpResponse(src)
@csrf_exempt
def login_SN(request):
        if SN.login():
                return HttpResponse("success")

@csrf_exempt
def get_JD(request):
        src = JD.get_src()
        print(src)
        return HttpResponse(src)
@csrf_exempt
def login_JD(request):
        if JD.login():
                return HttpResponse("success")
@csrf_exempt
def down(request):
        data = json.load(request)
        account = data.get('account')
        user = User.objects.filter(username=account).first()
        cars = Car.objects.filter(user_id=user)
        goods_down = []
        for car in cars:
                goods = {}
                good = Goods.objects.filter(id=car.good_id.id).first()
                price_id = good.price_queue_id
                if price_id == 0:
                        rec_price = good.good_price4
                        pre_price = good.good_price3
                elif price_id == 1:
                        rec_price = good.good_price0
                        pre_price = good.good_price4
                elif price_id == 2:
                        rec_price = good.good_price1
                        pre_price = good.good_price0
                elif price_id == 3:
                        rec_price = good.good_price2
                        pre_price = good.good_price1
                else:
                        rec_price = good.good_price3
                        pre_price = good.good_price2
                rec_price = re.search(r"(\d+(\.\d{2})?)", rec_price).group(1)
                pre_price = re.search(r"(\d+(\.\d{2})?)", pre_price).group(1)
                rec_price = float(rec_price)
                pre_price = float(pre_price)
                if rec_price < pre_price and rec_price!=0:
                        if good.good_from == 'JD':
                                goods['from'] = '京东'
                        elif good.good_from == 'SN':
                                goods['from'] = '苏宁'
                        else:
                                goods['from'] = '唯品会'
                        goods['title'] = good.good_title
                        goods['pre_price'] = pre_price
                        goods['rec_price'] = rec_price
                        goods_down.append(goods)
                else:
                        continue
        print(goods_down)
        return JsonResponse(goods_down, safe=False)

@csrf_exempt
def get_account(request):
    data = json.loads(request.body)
    account = data.get('account')
    user = User.objects.filter(username=account).first()
    date_joined = user.date_joined

    chinese_time_str = date_joined.strftime("%Y.%m.%d %A %H:%M:%S")

    information= {'account': user.username,'email':user.email,'date_joined':chinese_time_str}
    print(user.date_joined)
    return JsonResponse(information, safe=False)
@csrf_exempt
def get_price(request):
        check_price()
        return HttpResponse("价格检查完成")

@csrf_exempt
def send_email(request):
        send_emails()
        return HttpResponse("发送降价提醒完成")