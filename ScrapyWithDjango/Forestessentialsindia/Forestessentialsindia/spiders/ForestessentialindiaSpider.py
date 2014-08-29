from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Forestessentialsindia.items import  ForestessentialsindiaItem
import re, sys, os

sys.path.append('pathtoproject')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parsing.settings")

from product.models import Product

class  ForestessentialsindiaSpider (CrawlSpider) :
  handle_httpstatus_list = [302]
  name = "fei"
  allowed_domains = ["forestessentialsindia.com"]
  start_urls = ['http://www.forestessentialsindia.com/products/by-category/body-care.html',
		'http://www.forestessentialsindia.com/products/by-category/facial-care.html',
		'http://www.forestessentialsindia.com/products/by-category/hair-care.html',
		'http://www.forestessentialsindia.com/products/by-category/wellness.html'
						]

  rules = (
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/wellness.*\.html", ), unique=True), callback='parse_item', follow= True),
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/hair-care.*\.html", ), unique=True ), callback='parse_item', follow= True),
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/facial-care.*\.html", ), unique=True ), callback='parse_item', follow= True),
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/body-care.*\.html", ), unique=False), callback='parse_item',  follow= True),
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/body-care\.html\?p=\d+", ), unique=False), callback='parse_item',  follow= True),
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/facial-care\.html\?p=\d+", ), unique=False), callback='parse_item',  follow= True),
      Rule(SgmlLinkExtractor(allow=("http://www.forestessentialsindia.com/products/by-category/hair-care\.html\?p=\d+", ), unique=False), callback='parse_item',  follow= True),
  )
  def parse_item(self, response) :
    sel = Selector (response)
    item =  ForestessentialsindiaItem ()
    item['Source_Website'] = "http://www.forestessentialsindia.com"
    item['Title'] = str (map(unicode.strip, sel.xpath ('//div[@class="product-name"]//text()').extract())).replace ("[u'", "").replace ("[u", "").replace("'","").replace ("'],", "").replace(" u","").replace ("]'", "").replace("}", "").replace(",]","").replace(",","")
    item['Category'] = str (sel.xpath ('//div[@class="breadcrumbs"]/ul/li/a/text()').extract()).replace ("[u'", "").replace ("[u", "").replace("'","").replace ("'],", "").replace(" u","").replace ("]'", "").replace ("]", "")
    item['Product_URL'] = response.request.url
    item['Description'] = str(map(unicode.strip, sel.xpath ('//div[@class="short-description2 product_detail_scrollbar product_detail_scrollbar_detail"][@id="product_detail_scrollbar"]//text()').extract ())).replace ("[u'", "").replace ("[u", "").replace("'","").replace ("'],", "").replace(" u","").replace ("]'", "").replace ("]", "").replace(",","")
		
    item['Details'] = str (map(unicode.strip, sel.xpath ('//div[@id="feview"]//text()').extract ())).replace ("[u'", "").replace ("[u", "").replace("'","").replace ("'],", "").replace(" u","").replace ("]'", "").replace ("]", "").replace(",","")
    DESC = ""
    DESC = item['Description'] + item['Details']
    item['Image_URL'] =  str (sel.xpath ('//div[@class="product-img-box"]/a/@href').extract()).replace ("[u'", "").replace ("']", "")
    price = str (sel.xpath ('//span[@class="regular-price"]/span[@class="price"]/text()').extract())
    price = re.findall ('\d+,*\d+', price)
    Flag = True
    if len (price) > 1 or (price == None) :
      Flag = False
    item['Price'] = str (price)
    price = str (price)

    if item['Title'] and item['Description'] and Flag and price != None:    
      item1 = Product() 
      item1.brand_name = "Forest Essential India"
      item1.code = item['Title']
      item1.title = item['Title']
      item1.description = DESC
      item1.category_name = item['Category']
      try :
        price = price.replace(",","").replace("'","").replace("[","").replace("]","").replace(" u","")
        item1.original_price =  float (price )
        item1.price = float (price)
      except :
        pass
      item1.source_id = 10
      item1.image_url1 = item['Image_URL']
      item1.source_url = item['Product_URL']
      item1.save() 
    if item['Title'] and item['Description']:
        return item

