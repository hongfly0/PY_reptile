#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib
import urllib.request
from lxml import etree
from os import system
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


pciturelist=[]

header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            , "Connection": "keep-alive"
         }

star_name = 'pengyuyan'

base_url = 'https://www.aitaotu.com'

url = ''


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



"""
获取单个写真中的图片
"""
def getInfos(info_url) :

    info_path = getRequestResult(base_url+info_url)
    



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



print('开始')
getPageList();
print('结束')
