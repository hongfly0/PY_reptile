# -*- coding: utf-8 -*-
"""
查询京东 获取京东价格 并写入数据库
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
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "168168", "pythontest")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
db.close()

