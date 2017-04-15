__author__ = 'Administrator'
# -*-coding: utf-8 -*-
import xlrd
#import MySQLdb
import redis
# Open the workbook and define the worksheet
book = xlrd.open_workbook(r"/Users/maomao/Desktop/virus_ad.xls")
sheet = book.sheet_by_name("sheet1")

producer_pool = redis.ConnectionPool(host="192.168.3.70", port=6379, db=0)
producer = redis.Redis(connection_pool=producer_pool)

for r in range(1, sheet.nrows):
      id   = sheet.cell(r,0).value
      producer.lpush('apk_name', id)
      '''file_checksum = sheet.cell(r,2).value.lower()
      Viruses  = sheet.cell(r,3).value
      category  = sheet.cell(r,4).value
      platform = sheet.cell(r,5).value
      description  = sheet.cell(r,6).value
      download_url = sheet.cell(r,7).value
      values = (id, store_display_name, file_checksum, Viruses, category, platform,  description, download_url)'''
print ""
print "Done! "
print ""
columns = str(sheet.ncols)
rows = str(sheet.nrows)
