from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep
import re
import json

src = 0

def search_good(goods):
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
    with open("./web/cookies_A.json", "r") as file:
        cookies = json.load(file)
    url = "https://www.vip.com/"
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    url = "https://category.vip.com/suggest.php?keyword=%s" % goods
    driver.get(url)
    for i in range(6):
        distance = i * 800
        js = "document.documentElement.scrollTop=%d" % distance
        driver.execute_script(js)
        sleep(0.4)
    html = etree.HTML(driver.page_source)

    driver.quit()
    li_list = html.xpath(
        '//section[@class="goods-list c-goods-list--normal"]/div[@class="c-goods-item  J-goods-item c-goods-item--auto-width"]'
    )
    counter = 0
    goods_all = []
    for li in li_list:
        if counter < 40:
            counter = counter + 1
        else:
            break
        dic = {}
        dic["id"] = li.xpath("./@data-product-id")[0]
        goods_img = li.xpath('./a/div/div[@class="c-goods-item__img"]/img/@src')
        dic["img"] = "https:" + goods_img[0]
        title = li.xpath(
            './a/div/div[@class="c-goods-item__name  c-goods-item__name--two-line"]/text()'
        )
        if not title:
            title = li.xpath(
                './a/div/div[@class="c-goods-item__name  c-goods-item__name--one-line"]/text()'
            )
        dic["title"] = "".join(title)
        dic["price"] = "".join(
            li.xpath(
                './a/div/div/div/div[@class="c-goods-item__sale-price J-goods-item__sale-price"]/text()'
            )
        )
        dic["link"] = "https:" + "".join(li.xpath("./a/@href"))
        goods_all.append(dic)
    return goods_all

def login():
    global src
    src=0
    url = "https://passport.vip.com/login"
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
    driver.get(url)
    html = etree.HTML(driver.page_source)
    sleep(0.5)
    src = html.xpath('//div[@class="c-qr-img-wrapper  J-qr-img-wrapper"]/img/@src')[0]
    wait = WebDriverWait(driver, 60)
    try:
        wait.until(EC.url_to_be("https://www.vip.com/"))
    except Exception as e:
        print("还未登录")
    if driver.title != "唯品会网站登录":
        cookies = driver.get_cookies()
        with open("./web/cookies_A.json", "w") as file:
            json.dump(cookies, file, indent=4)
        src = 0
        return True

def get_src():
    global src
    while src ==0:
        pass
    re_src = src
    sec =0
    return re_src