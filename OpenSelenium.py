"""
爬虫工具 selenium 测试demo
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import urllib
import urllib.request
import random
import time
from lxml import html
import unittest
from selenium.common.exceptions import NoSuchElementException

import os

global save_path
save_path = 'instagram'

global tag

tag = 'ogurayuka_official'



"""
创建文件夹
"""


def mkdir(title):
    pathdir = os.path.split(os.path.realpath(__file__))[0] + '/instagram/' + title

    path = pathdir.strip()
    path = path.rstrip("/")
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        print(path + ' 创建成功')
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
    return pathdir


"""
下载图片到本地
"""


def getImage(now_image_src, download_dir, file_name='111'):

    download_url = file_name

    i = 0
    for image_url in now_image_src :
        file_name = file_name + '_' + str(i)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 \
            Safari/537.36"
            , "Connection": "keep-alive"
            , "Referer": "image / webp, image / *, * / *;q = 0.8"
            , "Accept": "image/webp,image/*,*/*;q=0.8"
        }

        # try:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 \
            Safari/537.36"
            , "Connection": "keep-alive"
            , "Referer": image_url
        }

        file = download_dir + '/' + file_name + '.jpg'

        if os.access(file, os.F_OK):
            print(file_name + '.jpg 已存在')
        else:
            req = urllib.request.Request(image_url, headers=headers)
            urlhtml = urllib.request.urlopen(req)
            respHtml = urlhtml.read()

            binfile = open(file, "wb")
            binfile.write(respHtml);
            binfile.close();
            print(file + ' | success')
            random_wait = random.randint(2, 6)
            time.sleep(random_wait)
            print('等待 '+str(random_wait))

        global tag
        fw = open("inscheck_txt/"+tag+".txt", mode='w')
        fw.write(download_url )
        print("完成连接：/p/" + download_url+'/')
        fw.close()



def getInfo(driver):
    time.sleep(6)
    source_data = driver.page_source
    htmlXml = html.fromstring(source_data)

    images_info = htmlXml.xpath('//div[@class="ZyFrc"]//img/@src')

    current_url_name = driver.current_url.split('/')[4]

    print(images_info)

    global save_path

    print('开始下载....')

    getImage(images_info,save_path,current_url_name)

    if checkIsExist(driver, 'coreSpriteRightPaginationArrow'):
        rollNextInfo(driver)
    else:
        print('没有更多了')
        return

"""
翻到下一个动态
"""
def rollNextInfo(driver) :
    print('下一个动态')
    driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
    time.sleep(5)

    getInfo(driver)



"""
翻到下一个图片 
"""
def rollNextImage(driver) :

    driver.find_element_by_class_name('coreSpriteRightChevron').click()

    time.sleep(3)

    getImage('2', '111')

    print(checkIsExist(driver,'coreSpriteRightChevron'))

    if checkIsExist(driver,'coreSpriteRightPaginationArrow'):
        rollNextInfo(driver)
    else:
        print('没有更多了')
        return


"""
检测元素是否存在
"""
def checkIsExist(driver,class_name) :
    return_bool = 'false'
    try:
        if driver.find_element_by_class_name(class_name) :
            return_bool = 1

    except NoSuchElementException :
        return_bool = 0

    return return_bool


"""
下翻到历史下载的页数
"""
def rollHistory(driver,href_url) :

    print('去到上一次停止的地方:'+href_url)

    href_url = '/p/'+href_url+'/'

    is_stop = 0
    i= 1

    while is_stop == 0:
        print('第'+str(i) + '次滚动')
        js = "var q=document.documentElement.scrollTop=100000"
        driver.execute_script(js)
        time.sleep(3)
        i += 1

        try:
            if driver.find_element_by_xpath('//a[@href="'+href_url+'"]'):
                is_stop = 1
                driver.find_element_by_xpath('//a[@href="' + href_url + '"]').click()
        except NoSuchElementException:
            is_stop = 0
            continue

        return


if __name__ == '__main__':
    # tag = input('请输入需要搜索的关键字:')

    #ins_url = 'https://www.instagram.com/'+tag+'/'

    ins_url = 'https://www.instagram.com/ogurayuka_official/'

    save_path = mkdir(tag)

    # 1. 创建浏览器对象
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")

    # 2. 发送请求
    driver.get(ins_url)

    # 3. 等待10秒时间
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'KL4Bh')))

    list_history = []

    if os.path.exists("inscheck_txt/"+tag+".txt") :
        f = open("inscheck_txt/"+tag+".txt", mode='r')
        list_history = f.readlines()
    else :
        f = open("inscheck_txt/" + tag + ".txt", mode='w')

    f.close()

    if len(list_history)>0:
        #获取历史记录，并且去到上次下载的地方
        rollHistory(driver,list_history[0])
    else:
        class_click = driver.find_element_by_class_name('eLAPa')
        class_click.click()  # 模拟点击,可以模拟点击加载更多

    getInfo(driver)

    print('抓取结束')
    #关闭浏览器
    driver.quit()
