from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep
import re
import json

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
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(3)
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