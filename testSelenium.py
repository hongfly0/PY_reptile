"""
爬虫工具 selenium 测试demo
"""
from  selenium import webdriver
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

tag = 'gakki_smile'

roll_times = int(input('请输入要滚动的次数:'))

"""
循环次数 ，翻动网页
"""
def rollPage(driver,times) :

    for i in range(times) :
        print('第'+str(i+1)+'次 滚动')
        js = "var q=document.documentElement.scrollTop=100000"
        run_res = driver.execute_script(js)

        randnum = random.randint(2,6)

        print('休息'+str(randnum)+'秒')

        time.sleep(randnum)


"""
创建文件夹
"""
def mkdir(title):
    pathdir =  os.path.split(os.path.realpath(__file__))[0]+'/instagram/'+title

    path=pathdir.strip()
    path=path.rstrip("/")
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        print(path+' 创建成功')
        os.makedirs(path)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
    return pathdir


"""
下载图片到本地
"""
def getImage(now_image_src,download_dir,file_name) :
    print('下载：'+ now_image_src)

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer": "image / webp, image / *, * / *;q = 0.8"
        , "Accept": "image/webp,image/*,*/*;q=0.8"
    }

    # try:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
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


if __name__ == '__main__':
    save_path = mkdir(tag)

    # 1. 创建浏览器对象
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")

    # 2. 发送请求
    driver.get('https://www.instagram.com/'+tag+'/')

    # 3. 等待10秒时间
    wait = WebDriverWait(driver,10)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'KL4Bh')))

    # 使用js 拉取页面到最底部
    rollPage(driver,roll_times)

    # 4. 获取页面
    print('正在获取页面信息....')
    data = driver.page_source
    htmlXml = html.fromstring(data)

    htmlfile = open('ins.html','w')
    htmlfile.write(str(htmlXml))
    htmlfile.close()

    images_infos = htmlXml.xpath('//div[@class="KL4Bh"]/img/@src')

    print('总共获取到' + str(len(images_infos)) + '张照片')
    print(images_infos)

    # i = 0
    #
    # while i < len(images_infos) :
    #     print('开始下载图片：'+images_infos[i])
    #
    #     getImage(images_infos[i],save_path,str(i))
    #     # 获取随机数 下载完成之后  随机休息 1-6秒 减少访问次数
    #     randnum = random.randint(1,6)
    #
    #     print('下载完成,休息'+str(randnum)+'(s)')
    #
    #     time.sleep(randnum)
    #     i += 1


    print('抓取结束')



