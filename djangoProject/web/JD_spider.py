from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep
import json

src = 0
def login():
    url = "https://passport.jd.com/new/login.aspx"
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
    button = driver.find_element(By.XPATH, '//a[@clstag="pageclick|keycount|passport_main|click_wx_login"]')
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
        wait.until(EC.title_is("京东(JD.COM)-正品低价、品质保障、配送及时、轻松购物！"))
    except Exception as e:
        print("还未登录")
    if driver.title != "京东-欢迎登录" and driver.title != "微信登录":
        cookies = driver.get_cookies()
        with open("./web/cookies_JD.json", "w") as file:
            json.dump(cookies, file, indent=4)
        src = 0
        return True


def get_src():
    global src
    while src ==0:
        pass
    return src

def search_goods(goods):
    options = EdgeOptions()
    # options.add_argument("--headless")
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
    url = "https://www.jd.com"
    driver.get(url)
    with open("./web/cookies_JD.json", "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    url = "https://search.jd.com/Search?keyword=%s" % goods
    driver.get(url)
    html = etree.HTML(driver.page_source)
    driver.quit()
    li_list = html.xpath('//ul[@class="gl-warp clearfix"]/li')
    goods_all = []
    for li in li_list:
        dic = {}
        dic["id"] = li.xpath('./div/div[@class="p-price"]/strong/i/@data-price')[0]
        goods_img = li.xpath('./div/div[@class="p-img"]/a/img/@src')
        if not goods_img:
            goods_img = li.xpath('./div/div[@class="p-img"]/a/img/@data-lazy-img')
        dic["img"] = "https:" + goods_img[0]
        title = li.xpath('./div/div[@class="p-name"]/a/em/text()')
        if not title :
            title = li.xpath('.//div/div[@class="p-name"]/a/em//font/text() | .//div/div[@class="p-name"]/a/em/text()')
        if not title:
            title = li.xpath(
                './/div/div[@class="p-name p-name-type-2"]/a/em//font/text() | .//div/div[@class="p-name p-name-type-2"]/a/em/text()'
            )
        dic["title"] =''.join(title)
        dic["shop"] = ''.join(li.xpath('./div/div[@class="p-shop"]/span/a/text()'))
        dic["price"] = li.xpath('./div/div[@class="p-price"]/strong/i/text()')[0]
        dic["link"] = "https:" + "".join(
            li.xpath('./div/div[@class="p-name p-name-type-2"]/a/@href')
        )
        goods_all.append(dic)
    return goods_all