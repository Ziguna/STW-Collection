# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HimalayawellnessItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	Title = Field ()
	Source_Website = Field ()
	Product_URL = Field ()
	Price = Field ()
	Description = Field ()
	Image_URL = Field ()
	Category = Field ()
	Size = Field ()
	pass
