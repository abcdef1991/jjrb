# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

class JjrbnewsPipeline(object):
    def process_item(self, item, spider):
        return item

class JjrbpaperInfoPipeline(object):
    #将解析出的内容以txt文件的形式保存在content文件夹
    def open_spider(self, spider):
        today = datetime.date.today() + datetime.timedelta(days=-1)
        date = today.strftime(r'%Y-%m-%d')
        filename = 'content\JjrbpaperInfo' + date + '.txt'
        self.f = open(filename, 'w')
 
    def close_spider(self, spider):
        self.f.close()
 
    def process_item(self, item, spider):
        try:
            line = str(dict(item)) + '\n'
            self.f.write(line)
        except:
            pass
        return item 