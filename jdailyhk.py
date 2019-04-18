# -*- coding: utf-8 -*-
"""
拉取 https://jdailyhk.com/
香港人的青春期杂志
"""
import urllib
import urllib.request
from lxml import etree
from os import system
import random
import time
import ssl
from urllib.parse import quote
import string


ssl._create_default_https_context = ssl._create_unverified_context

import os

start_url = 'https://jdailyhk.com/2018/10/korean_leggings/';

header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            , "Connection": "keep-alive"
         }

global save_img_path
save_img_path = ""

def Info() :
    req = urllib.request.Request(start_url, headers=header)
    html = urllib.request.urlopen(req)
    htmldata = html.read().decode('utf-8')

    fw = open("jdailyhk.html", mode='w',encoding='utf-8')
    fw.write(htmldata)
    fw.close()

    htmlpath = etree.HTML(htmldata)

    title_arr =  htmlpath.xpath('//title/text()')
    title = title_arr[0].replace(" ","")
    title = title.replace("|Jdailyhk", "")

    if len(title) > 0 :
        global save_img_path
        save_img_path = mkdir(title)

        #获取封面图片
        cover_image = htmlpath.xpath('//div[@class="td-post-featured-image"]/a/@href')

        getImage(cover_image,save_img_path,'cover')

        images = htmlpath.xpath('//img[contains(@class, "alignnone") and contains(@class, "size-full")]/@src')
        content = htmlpath.xpath('//div[contains(@class, "td-post-content")]')

        fc = open(save_img_path+'/content.txt',mode='w',encoding='utf-8')
        fc.write(content[0].xpath('string(.)').strip())
        fc.close()

        getImage(images,save_img_path,title)

        #完成之后 记录下载成功的title
        fw = open("jdailyhk_finished.txt", mode='a', encoding='utf-8')
        fw.write(title+'\n')
        fw.close()

    else :
        print('获取页面错误')


def mkdir(title):
    pathdir = os.path.split(os.path.realpath(__file__))[0] + '/jdaliyhk/' + title

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


def getImage(now_image_src, download_dir, file_name_old='111'):

    download_url = file_name_old

    i = 0
    for image_url in now_image_src :
        image_url_new = quote(image_url, safe=string.printable)

        file_name = file_name_old + '_' + str(i)

        file_type_arr = image_url.split('.')
        file_type = file_type_arr[int(len(file_type_arr))-1]

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
            , "Referer": image_url_new
        }

        file = download_dir + '/' + file_name + '.'+file_type

        if os.access(file, os.F_OK):
            print(file_name + '.jpg 已存在')
        else:
            try:
                req = urllib.request.Request(image_url_new, headers=headers)
                urlhtml = urllib.request.urlopen(req)
                respHtml = urlhtml.read()
            except:
                print('请求异常')
                continue

            binfile = open(file, "wb")
            binfile.write(respHtml)
            binfile.close()
            print(file + ' | success')
            random_wait = random.randint(2, 6)
            print('等待 '+str(random_wait))
            time.sleep(random_wait)

        i += 1

Info();
print('下载结束')