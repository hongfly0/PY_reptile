#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib
import urllib.request
from lxml import etree
from os import system
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

import os


pciturelist=[]

header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            , "Connection": "keep-alive"
         }

star_name = 'pengyuyan'

base_url = 'https://www.aitaotu.com'

url = ''

global save_path
save_path = os.path.split(os.path.realpath(__file__))[0] + '/aitaotu/'+star_name+'/'

global download_path
download_path = ''


"""
获取目标分页
"""
def  getPageList():
    global  url
    url = base_url + '/tag/' + star_name + 'tupian.html'

    page_html_path = getRequestResult(url)
    page_list_path = page_html_path.xpath('//div[@id="pageNum"]/span/a/@href')

    page_list = python_array_unique(page_list_path)
    #在数组的最开头增加一个元素
    page_list.insert(0,'/tag/'+star_name+'tupian/1.html')

    getListFromList(page_list)


"""
获取单页元素集合
"""
def getListFromList(list) :

    for url_value  in  list:
        info_list_path = getRequestResult(base_url+url_value)
        info_list = info_list_path.xpath('//a[@class="Pli-litpic"]/@href')

        for info_url in info_list :
            global download_path
            download_path = ''
            getInfos(info_url)


"""
获取单个写真中的图片
"""
def getInfos(info_url) :
    info_path = getRequestResult(base_url+info_url)

    page_list = info_path.xpath('//div[@class="pages"]/ul/li/a/@href')

    title = info_path.xpath('//div[@id="photos"]/h1/text()')[0]

    global download_path
    download_path = mkdir(title);

    now_image_url = info_path.xpath('//div[@id="big-pic"]/p/a/img/@src')[0]
    getImage(now_image_url, download_path, '1')

    if len(page_list) == 0 :
        print(title + '写真集获取结束')
        return
    else :
        last_page = page_list[-1]
        str_page_array = last_page.split('.')
        str_page_array_2 = str_page_array[0].split('_')
        total_page = str_page_array_2[1]

        print('total_page :' + total_page)

        getInfoImages(info_url,total_page)

    print(title + '写真集获取结束')


"""
获取多页写真
"""
def getInfoImages(start_url,total_page) :
    i = 2
    print(start_url)
    while i <= int(total_page) :
        now_info_url = start_url.replace('.html','_'+str(i)+ '.html')
        info_path = getRequestResult(base_url + now_info_url)
        now_image_url = info_path.xpath('//div[@id="big-pic"]/p/a/img/@src')[0]

        getImage(now_image_url,download_path,str(i))
        i += 1
        time.sleep(0.5)


    
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


"""
根据url 获取url目标的结果集
"""
def getRequestResult(url) :
    page_req = urllib.request.Request(url, headers=header)
    page_html = urllib.request.urlopen(page_req)
    page_html_data = page_html.read()
    page_html_path = etree.HTML(page_html_data)

    return page_html_path

"""
去除重复元素
"""
def python_array_unique(array) :
    new_array = []

    for element in  array :
        if(element not in new_array):
            new_array.append(element)

    return new_array


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


print('开始')
getPageList();
print('结束')
