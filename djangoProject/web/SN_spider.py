from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep
import re
import json
src = 0

def search_good(goods):
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=ImagesEnabled")
    options.add_argument("--disable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Edge(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
        },
    )
    url = "https://search.suning.com/%s/" % goods
    driver.get(url)
    for i in range(6):
        distance = i * 800
        js = "document.documentElement.scrollTop=%d" % distance
        driver.execute_script(js)
        sleep(0.8)
    html = etree.HTML(driver.page_source)
    li_list = html.xpath('//ul[@class="general clearfix"]/li')
    driver.quit()
    counter = 0
    good_all = []
    for li in li_list:
        if counter < 40:
            counter=counter+1
        else:
            break
        dic = {}
        dic["id"] = li.xpath("./@id")[0]
        goods_img = li.xpath('./div/div/div[@class="res-img"]/div/a/img/@src')
        dic["img"] = "https:" + goods_img[0]
        title = li.xpath(
            './div/div/div[@class="res-info"]/div[@class="title-selling-point"]/a/text()'
        )
        dic["title"] = "".join(title)
        dic["shop"] = "".join(
            li.xpath(
                './div/div/div[@class="res-info"]/div[@class="store-stock"]/a/text()'
            )
        )
        dic["price"] = "".join(
            li.xpath(
                './div/div/div[@class="res-info"]/div[@class="price-box"]/span/i/text()|./div/div/div[@class="res-info"]/div[@class="price-box"]/span/text()'
            )
        )
        # print(dic["price"])
        dic["price"] = dic["price"][2:]
        dic["link"] = "https:" + "".join(
            li.xpath(
                './div/div/div[@class="res-info"]/div[@class="title-selling-point"]/a/@href'
            )
        )
        good_all.append(dic)
    return good_all

def login():
    url = "https://passport.suning.com/ids/login"
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=ImagesEnabled")
    options.add_argument("--disable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Edge(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
        },
    )
    driver.get(url)
    button = driver.find_element(By.XPATH, '//a[@aria-label="微信联合登录"]')
    button.click()
    wait = WebDriverWait(driver, 360)
    try:
        wait.until(EC.title_is("微信登录"))
    except Exception as e:
        print("还未跳转")
    html = etree.HTML(driver.page_source)
    sleep(0.5)
    global src
    src = "https://open.weixin.qq.com"+html.xpath('//div[@class="web_qrcode_img_wrp"]/img/@src')[0]
    try:
        wait.until(EC.title_is("苏宁易购(Suning.com)-换新到苏宁 省钱更省心！"))
    except Exception as e:
        print("还未登录")
    if driver.title != "用户登录" and driver.title != "微信登录":
        cookies = driver.get_cookies()
        with open("./web/cookies_SN.json", "w") as file:
            json.dump(cookies, file, indent=4)
        src = 0
        return True


def get_src():
    global src
    while src ==0:
        pass
    return src