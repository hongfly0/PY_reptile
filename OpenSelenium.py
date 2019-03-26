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

import os

global save_path
save_path = 'instagram'

#tag = input('请输入需要搜索的关键字:')

tag = '彭于晏'

# gakki_smile 新恒结衣
# luoyiyi1007 张艺兴


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
def getImage(now_image_src, download_dir, file_name):
    print('下载：' + now_image_src)

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
        , "Referer": now_image_src
    }

    file = download_dir + '/' + file_name + '.jpg'

    if os.access(file, os.F_OK):
        print(file_name + '.jpg 已存在')
    else:
        req = urllib.request.Request(now_image_src, headers=headers)
        urlhtml = urllib.request.urlopen(req)
        respHtml = urlhtml.read()

        binfile = open(file, "wb")
        binfile.write(respHtml);
        binfile.close();
        print(file + ' | success')


def getInfo(driver,source_data) :

    htmlXml = html.fromstring(source_data)

    images_info = htmlXml.xpath('//div[@class="KL4Bh"]/img/@src')

    time.sleep(2)

    # 检测有没有下一页的按钮
    check_next_image = driver.find_element_by_class_name(By.XPATH,'//button[@class="_6CZji"]')

    print(check_next_image)

    if len(images_info) == 0 :
        #翻到下一个动态
        print('翻到下一个动态')

    time.sleep(2)




    click_new_image = driver.find_element_by_class_name('_6CZji')
    click_new_image.click()  # 模拟点击,可以模拟点击加载更多


    # if click_new_image > 0 :
    #     print('下载图片，下载完成后 翻到下一页')
    # else :
    #     #翻到下一个动态
    #     print('翻到下一个动态')










if __name__ == '__main__':
    save_path = mkdir(tag)

    # 1. 创建浏览器对象
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")

    # 2. 发送请求
    driver.get('https://www.instagram.com/explore/tags/' + tag + '/')

    # 3. 等待10秒时间
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'KL4Bh')))

    class_click = driver.find_element_by_class_name('eLAPa')
    print(class_click)
    class_click.click()  # 模拟点击,可以模拟点击加载更多
    data = driver.page_source

    getInfo(driver,data)

    # 4. 获取页面
    print('正在获取页面信息....')
    htmlfile = open('ins.html', 'w')
    htmlfile.write(str(data.encode('UTF-8')))
    htmlfile.close()

    htmlXml = html.fromstring(data)


    print('抓取结束')
    # 关闭浏览器
    #driver.quit()
