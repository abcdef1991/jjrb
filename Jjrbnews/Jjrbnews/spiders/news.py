# -*- coding: utf-8 -*-
import scrapy
import datetime
#from bs4 import BeautifulSoup
#import re

class NewsSpider(scrapy.Spider):
    name = "news"
    #allowed_domains = ["jjrb.cn"]
    today = datetime.date.today() + datetime.timedelta(days=-1)
    date = today.strftime(r'%Y-%m/%d/')
    head = 'http://jjrb.jjxw.cn/html/'
    last = 'node_1.htm'
    url = head + date + last
    start_urls = [url]
    
    
    #根据每日的首页url获取各个版面的url
    def parse(self, response):
        today = datetime.date.today() + datetime.timedelta(days=-1)
        date = today.strftime(r'%Y-%m/%d/')
        head = 'http://jjrb.jjxw.cn/html/'
        #html = response.body
        #soup = BeautifulSoup(html,'html.parser')
        #a = soup.find('div',id='bmlistbar').find_all('a',href=re.compile(r'node\w+'))
        body = response.css('div[id=bmlistbar]')
        a = body.css('a[href*=node]::attr(href)').extract()
        for href in a:
            try:
                #href = i['href']
                url = head + date + href
                yield scrapy.Request(url, callback=self.parse_news)
            except:
                continue
            
            
    #根据每个版面的url获得该版面所有文章的url        
    def parse_news(self, response):
        today = datetime.date.today() + datetime.timedelta(days=-1)
        date = today.strftime(r'%Y-%m/%d/')
        #html = response.body
        #soup = BeautifulSoup(html,'html.parser')
        #a = soup.find('div',id='main-ed-articlenav-list').find('tbody').find_all('a')
        body = response.css('div[id=main-ed-articlenav-list]')
        a = body.css('a::attr(href)').extract()
        for href in a:
            try:
                #href = i['href']
                url = 'http://jjrb.jjxw.cn/html/' + date + href
                yield scrapy.Request(url, callback=self.parse_article)
            except:
                continue
            
            
    #根据文章的url解析内容信息，如果为空，则输出空字符    
    def parse_article(self,response):
        infoDict = {}
        #html = response.body
        #soup = BeautifulSoup(html,'html.parser')
        
        try:
            #文章URL地址
            url = response.url.strip()
        except:
            url = ''
            
        try:
            #排序
            rank = response.url[-5:-4]
        except:
            rank = ''
            
        try:
            #版面
            #page = soup.find('td',id='currentBM').string
            page = response.css('td[id=currentBM] strong::text').extract()[0]
            pagenum = page[-3:-1]
            #pagerank = soup.find('tr',id=re.compile(r'\w+{}'.format(pagenum))).find('a',id="pageLink").string.strip()
            page = response.css('tr[id*={}]'.format(pagenum))
            pagerank = page.css('a[id=pageLink]::text').extract()[0].strip()
        except:
            pagerank = ''
            
        try:
            #标题
            #title = soup.find('p',attrs={'class':'BSHARE_TEXT'}).text.strip()
            title = response.css('p[class=BSHARE_TEXT]::text').extract()[0]
        except:
            title = ''
            
        try:
            #正文
            content = []
            founder = response.css('founder-content p::text').extract()
            #soup.find('founder-content').find_all('p')
            for p in founder :
                content.append(p.replace(u'\xa0', u'').replace(u'\u3000',u''))
            text = ''.join(content)
        except:
            text = ''
        
        try:
            #图片
            pic = []
            #table = soup.find('table',attrs={'class':'wz'})
            #img = table.find_all('img')
            img = response.css('table[class=wz] img::attr(src)').extract()
            picurl = 'http://jjrb.jjxw.cn'
            if img != [] :
                for i in img :
                    pic.append(picurl + i[8:])
            else:
                pic = ''
        except:
            pic = ''
            
        try:
            #作者
            #author = soup.find('founder-author').text.strip()
            author = response.css('founder-author::text').extract()[0].strip()
        except:
            author = ''
            
        infoDict.update(
             {'title':title,'url':url,'author':author,'pagerank':pagerank,'rank':rank,'text':text,'pic':pic}
                         )
        yield infoDict
