# !/usr/bin/env python
# -*-coding:utf-8-*-
import urllib
import urllib.request
from lxml import etree
from os import system
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

import os

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    , "Connection": "keep-alive"
}

id = '90324'

global save_path
save_path = os.path.split(os.path.realpath(__file__))[0] + '/mzitu/'

def getTypePages():
    now_url = 'https://www.mzitu.com/' + id
    print('url:' + now_url)
    req = urllib.request.Request(now_url, headers=header)
    html = urllib.request.urlopen(req)
    htmldata = html.read()

    htmlpath = etree.HTML(htmldata)

    page_title = htmlpath.xpath('//h2[@class="main-title"]/text()')[0]

    pages = htmlpath.xpath('//div[@class="pagenavi"]/a/span/text()')

    frist_image_url = htmlpath.xpath('//div[@class="main-image"]/p/a/img/@src')[0]

    max_page = pages[4]

    if len(page_title) > 0:
        global save_path
        save_path = mkdir(page_title)
    else:
        print('找不到标题')
        return

    i = 2
    saveImage(frist_image_url, '1')
    next_url = ''

    while i <= int(max_page) :
        time.sleep(0.5)
        next_url = now_url + '/'+ str(i)
        getInfoImage(next_url,str(i))
        i = i+1


def getInfoImage(now_image, num):
    req_image_now = urllib.request.Request(now_image, headers=header)
    html_now = urllib.request.urlopen(req_image_now)
    html_now_data = html_now.read()
    html_now_path = etree.HTML(html_now_data)

    now_image_src = html_now_path.xpath('//div[@class="main-image"]/p/a/img/@src')[0]

    saveImage(now_image_src, num)


def saveImage(now_image_src, num):
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
    req = urllib.request.Request(now_image_src, headers=headers)

    urlhtml = urllib.request.urlopen(req)
    respHtml = urlhtml.read()

    file = save_path + '/' + num + '.jpg'

    if os.access(file, os.F_OK):
        print(num + '.jpg 已存在')
    else:
        binfile = open(file, "wb")
        binfile.write(respHtml);
        binfile.close();
        print(file + ' | success')

# except Exception:
#     pass


"""
参数 url : 每一个MM写真专辑图片集合的地址
通过穿过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址
"""


def mkdir(title):
    pathdir = save_path + title

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


print('开始...')
getTypePages();
print('結束')
