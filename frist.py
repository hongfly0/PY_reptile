#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib
import urllib.request
from lxml import etree
from os import system
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import os
"""
第一步: 从 http://www.zngirls.com/rank/sum/ 开始抓取MM点击头像的链接(注意是分页的)
#第二部  http://www.zngirls.com/girl/21751/ 抓取每一个写真集合的链接(注意是分页的)
#第三部 http://www.zngirls.com/g/19671/1.html 在写真图片的具体页面抓取图片(注意是分页的)
"""
pciturelist=[]


header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            , "Connection": "keep-alive"
         }

type = 'hanguo'

"""
从起始页面 http://www.zngirls.com/rank/sum/ 开始获取排名的页数和每一页的url
"""
def  mmRankSum():
    req = urllib.request.Request("http://www.zngirls.com/rank/"+type+"/", headers=header)
    html = urllib.request.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    #首先获取页码数,然后用循环的方式挨个解析每一个页面
    pages = htmlpath.xpath('//div[@class="pagesYY"]/div/a/@href')
    pages.insert(0,' ')
    pages = sorted(list(set(pages)))

    for i in range(len(pages) -2 ):
        pagesitem="https://www.zngirls.com/rank/"+type+"/"+ pages[i]
        mmRankitem(pagesitem,i)

"""
参数 url : 分页中每一页的具体url地址
通过穿过来的参数，使用  lxml和xpath 解析 html，获取每一个MM写真专辑页面的url
"""
def mmRankitem(url,page_num):
    req = urllib.request.Request(url, headers=header)
    html = urllib.request.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    pages_girl = htmlpath.xpath('//div[@class="rankli_imgdiv"]/a/@href')

    for i in range(len(pages_girl)):
        girl_url = "http://www.zngirls.com" + pages_girl[i]
        girl_no = pages_girl[i].replace('/girl/','').replace('/','')

        #检测是否已经拉取完毕
        fb_check = open("/images/check.txt", mode='w')

        



        setInfo(girl_url,str(page_num) +  str(i) +girl_no)

        print ("相册地址:http://www.zngirls.com/" + pages_girl[i]+"album/")
        getAlbums("http://www.zngirls.com/" + pages_girl[i]+"/album/",str(page_num) +  str(i) +girl_no)
       #print "http://www.zngirls.com/" + pages[i]


"""
参数 url : 每一个MM专辑的页面地址
通过穿过来的参数，获取每一个MM写真专辑图片集合的地址
"""
def getAlbums(girlUrl,girl_no):
    print(girlUrl)
    req = urllib.request.Request(girlUrl, headers=header)
    html = urllib.request.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)

    pages_albums = htmlpath.xpath('//div[@class="igalleryli_div"]/a/@href')

    for i in range(len(pages_albums)):
        getPagePicturess("http://www.zngirls.com/" + pages_albums[i],girl_no)


def setInfo(grilUrl,gril_no) :
    req = urllib.request.Request(grilUrl, headers=header)
    gril_html = urllib.request.urlopen(req)
    gril_htmldata = gril_html.read()
    gril_htmlpath = etree.HTML(gril_htmldata)

    path = mkdir(gril_no)

    rows = gril_htmlpath.xpath('//div[@class="infodiv"]/table/tr/td/text()')

    detial  = gril_htmlpath.xpath('//div[@class="infocontent"]/p/text()')

    fp = open(path+'/' + gril_no + ".txt", mode='w')

    for i in range(len(rows)):
        check_mod = i % 2

        fp.write(rows[i])

        if check_mod == 1 :
            fp.write('\n')
        else :
            fp.write('  :   ')

    fp.write('\n')

    for j in range(len(detial)):
        fp.write(detial[j])

    fp.close()


"""
参数 url : 每一个MM写真专辑图片集合的地址
通过穿过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址
"""
def getPagePicturess(albumsurl,girl_no):
    req = urllib.request.Request(albumsurl, headers=header)
    html = urllib.request.urlopen(req)
    htmldata = html.read()
    htmlpath = etree.HTML(htmldata)
    pages_pic = htmlpath.xpath('//div[@id="pages"]/a/@href')
    for i in range(len(pages_pic)-2):
        savePictures("http://www.zngirls.com" + pages_pic[i],girl_no)

"""
参数 url : 每一个MM写真专辑图片集合的地址
通过穿过来的参数，首先先获取图片集合的页数，然后每一页解析写真图片的真实地址
"""
def mkdir(title):
    pathdir =  os.path.split(os.path.realpath(__file__))[0]+'/images/'+title

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
参数 url : 每一个MM写真专辑图片集合的地址(进过分页检测)
通过穿过来的参数，直接解析页面，获取写真图片的地址，然后下载保存到本地。
"""
def savePictures(itemPagesurl,girl_no):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer": "image / webp, image / *, * / *;q = 0.8"
        ,"Accept":"image/webp,image/*,*/*;q=0.8"
    }
    try:
        req = urllib.request.Request(itemPagesurl, headers=header)
        html = urllib.request.urlopen(req)
        htmldata = html.read()
        htmlpath = etree.HTML(htmldata)
        print(itemPagesurl)
        pages_res = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@src')
        names = htmlpath.xpath('//div[@class="gallery_wrapper"]/ul/img/@alt')
        title = htmlpath.xpath('//div[@class="albumTitle"]/h1/text()')
        title = title[0]
        pic_path = mkdir(girl_no+'/'+title)
    except Exception:
        pass


    for i in range(len(pages_res)):
        print(pages_res[i])
        pciturelist.append(pages_res[i])

        try:

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
                , "Connection": "keep-alive"
                , "Referer": pages_res[i]
            }
            req = urllib.request.Request(pages_res[i], headers=headers)

            urlhtml = urllib.request.urlopen(req)

            respHtml = urlhtml.read()

            binfile = open(pic_path+'/%s.jpg' % (names[i]) , "wb")
            binfile.write(respHtml);
            binfile.close();
        except Exception :
            pass


mmRankSum()
print('结束')

"""
fl=open('list.txt', 'w')
for i in pciturelist:
    fl.write(i)
    fl.write("\n")
fl.close()
print '关机ing'
"""
# print ('finish')
# system('shutdown -s')