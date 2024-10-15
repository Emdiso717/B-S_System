from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from time import sleep
import json


def login():
    url = "https://passport.jd.com/new/login.aspx"
    options = EdgeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Edge(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
        },
    )
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 10, 0.1)
    success = True
    try:
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "我的京东")))
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "link-login")))
        print("Success")
        cookies = driver.get_cookies()
        with open("./web/cookies.json", "w") as file:
            json.dump(cookies, file, indent=4)
    except Exception as e:
        print("登录失败请重试", e)
        success = False
    driver.quit()
    return success


def search_goods(goods):
    options = EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Edge(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
        },
    )
    driver.maximize_window()
    url = "https://www.jd.com"
    driver.get(url)
    with open("./web/cookies.json", "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    search_box = driver.find_element(
        By.CSS_SELECTOR, "input[clstag='h|keycount|h|keycount|head|search_c']"
    )
    search_box.send_keys(goods)
    search_button = driver.find_element(
        By.CSS_SELECTOR, "button[clstag='h|keycount|h|keycount|head|search_a']"
    )
    search_button.click()
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(2)
    html = etree.HTML(driver.page_source)
    li_list = html.xpath('//ul[@class="gl-warp clearfix"]/li')
    goods_all = []
    for li in li_list:
        dic = {}
        dic["id"] = li.xpath('./div/div[@class="p-price"]/strong/i/@data-price')[0]
        goods_img = li.xpath('./div/div[@class="p-img"]/a/img/@src')
        if not goods_img:
            goods_img = li.xpath('./div/div[@class="p-img"]/a/img/@data-lazy-img')
        dic["img"] = "https:" + goods_img[0]
        dic["title"] = li.xpath(
            './div/div[@class="p-name p-name-type-2"]/a/em//text()'
        )[0]
        dic["shop"] = li.xpath('./div/div[@class="p-shop"]/span/a/text()')
        dic["price"] = li.xpath('./div/div[@class="p-price"]/strong/i/text()')[0]
        goods_sales = li.xpath('./div/div[@class="p-commit"]/strong/a/text()')
        if not goods_sales:
            goods_sales.append("未知")
        dic["sales"] = goods_sales[0]
        dic["link"] = "https:" + "".join(
            li.xpath('./div/div[@class="p-name p-name-type-2"]/a/@href')
        )
        goods_all.append(dic)
    print(goods_all)
    driver.quit()
    return goods_all