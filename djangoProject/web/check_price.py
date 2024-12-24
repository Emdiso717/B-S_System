from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep
import re
import json
from .models import Goods
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from  .models import Car

def send_emails():
    users = User.objects.all()
    for user in users:
        message = '您关注的商品：'
        cars = Car.objects.filter(user_id=user.id)
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
            if rec_price < pre_price and rec_price != 0:
                message= message  + good.good_title + "降价啦！！\n"
                print(message,user.email)
            else:
                continue
        if message != '您关注的商品：':
            subject = 'Price Sleuth 商品降价提醒'
            message = message+'请来 Price Sleuth 查看详情！！'
            from_email = '3220105929@zju.edu.cn'
            recipient_list = [user.email]
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )
            except BadHeaderError:
                # 处理错误，例如记录日志或通知用户
                print("Invalid header found.")
            except Exception as e:
                # 处理其他可能的错误
                print("Something went wrong:", e)



def check_price():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=ImagesEnabled")
    options.add_argument("--disable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(executable_path='/app/web/chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
        },
    )
    url = "https://www.suning.com"
    driver.get(url)
    with open("./web/cookies_SN.json", "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    all_goods = Goods.objects.filter(good_from = 'SN')
    for good in all_goods:
        url = good.good_link
        driver.get(url)
        sleep(0.5)
        html = etree.HTML(driver.page_source)
        price = html.xpath(
            ' //span[@class="mainprice"]/text() | //span[@class="mainprice"]/span/text()'
        )
        price = "".join(price)
        if not price:
            price = "0.00"
        print(price)
        good_pid = good.price_queue_id
        if good_pid == 0:
            good.good_price0 = price
            good.price_queue_id = 1
        elif good_pid == 1:
            good.good_price1 = price
            good.price_queue_id = 2
        elif good_pid == 2:
            good.good_price2 = price
            good.price_queue_id = 3
        elif good_pid == 3:
            good.good_price3 = price
            good.price_queue_id = 4
        else:
            good.good_price4 = price
            good.price_queue_id = 0
        good.save()
    url = "https://www.vip.com/"
    driver.get(url)
    with open("./web/cookies_A.json", "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    all_goods = Goods.objects.filter(good_from='A')
    for good in all_goods:
        url = good.good_link
        driver.get(url)
        sleep(0.5)
        html = etree.HTML(driver.page_source)
        price = html.xpath('//span[@class="sp-price"]/text()')
        price = "".join(price)
        if not price:
            price = "0.00"
        print(price)
        good_pid = good.price_queue_id
        if good_pid == 0:
            good.good_price0 = price
            good.price_queue_id = 1
        elif good_pid == 1:
            good.good_price1 = price
            good.price_queue_id = 2
        elif good_pid == 2:
            good.good_price2 = price
            good.price_queue_id = 3
        elif good_pid == 3:
            good.good_price3 = price
            good.price_queue_id = 4
        else:
            good.good_price4 = price
            good.price_queue_id = 0
        good.save()
    all_goods = Goods.objects.filter(good_from='JD')
    for good in all_goods:
        url = good.good_link
        url = url.replace("jd.com", "jdvvv.com")
        driver.get(url)
        sleep(1)
        html = etree.HTML(driver.page_source)
        price = html.xpath('//div[@id="Acontainertooltip"]/text()')
        times=0
        while not price and times < 15:
            times = times+1
            driver.get(url)
            sleep(1)
            html = etree.HTML(driver.page_source)
            price = html.xpath('//div[@id="Acontainertooltip"]/text()')
        price = "".join(price)
        if not price:
            price = "0.00"
        print(price)
        good_pid = good.price_queue_id
        if good_pid == 0:
            good.good_price0 = price
            good.price_queue_id = 1
        elif good_pid == 1:
            good.good_price1 = price
            good.price_queue_id = 2
        elif good_pid == 2:
            good.good_price2 = price
            good.price_queue_id = 3
        elif good_pid == 3:
            good.good_price3 = price
            good.price_queue_id = 4
        else:
            good.good_price4 = price
            good.price_queue_id = 0
        good.save()
