from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from HimalayaWellness.items import HimalayawellnessItem
from selenium import selenium
from selenium import webdriver
from scrapy.http import FormRequest
from scrapy import log
from time import strftime
from datetime import timedelta
from datetime import datetime
import datetime
from time import sleep
import time
import re

class HimalayaWellnessSpider (CrawlSpider) :
  handle_httpstatus_list = [302]
  name = "hw"
  allowed_domains = ["himalayastore.com"]
  start_urls = ['http://www.himalayastore.com/allproducts.htm']

  rules = (
      Rule(SgmlLinkExtractor(allow=(".*http://www.himalayastore.com/allproducts.htm.*", ), unique=True), callback='parse_item', follow= True),
      Rule(SgmlLinkExtractor(allow=(".*\.htm.*", ), unique=True ), callback='parse_item', follow= True),
  )
  def __init__(self):
    CrawlSpider.__init__(self)
    self.verificationErrors = []
    self.selenium = selenium("localhost", 4444, "*chrome", "http://www.himalayastore.com")
    self.selenium.start()

  def __del__(self):
    self.selenium.stop()
    print self.verificationErrors
    CrawlSpider.__del__(self)

  def parse_item(self, response) :
    sel = Selector (response)
    item = HimalayawellnessItem ()
    sel1 = self.selenium
    sel1.open(response.url)
    #Wait for javscript to load in Selenium
    time.sleep(2.5)
    #Do some crawling of javascript created content with Selenium
    item['Source_Website'] = "https://www.himalayastore.com"
    item['Title'] = sel1.get_text ('//*[@id="productinfomain"]/h1')
    item['Category'] = sel1.get_text ('//div[@id="breadcrum"]')
    item['Product_URL'] = response.request.url
    desc = str(sel.xpath ('//section[@id="productmain"]//p/text()').extract ())
    desc1 = ""

    for i in range (len (desc)) :
      if desc[i] == '\r\n' or desc[i] == '\n':
        continue
      else :
        desc1 += desc[i]
    item['Description'] = desc1
    item['Image_URL'] =  sel.xpath ('//*[@id="sidebarforproduct"]/img/@src').extract()
    if not item['Image_URL'] :
      item['Image_URL'] =  sel.xpath ('//*[@id="sidebarforproduct"]/h3/img/@src').extract()
    price1 = str (sel1.get_text ('//*[@for="price"][@class="control-label1"]'))
    item['Price'] = price1
    item['Size'] = sel1.get_text ('//*[@id="size_type"]')
    return item






