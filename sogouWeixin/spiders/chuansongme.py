# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from sogouWeixin.items import ChuansongmeItem

class ChuansongmeSpider(CrawlSpider):
    name = 'chuansongme'
    allowed_domains = ['chuansongme.com']
    start_urls = ['http://chuansongme.com/accounts']

    rules = (
        Rule(LinkExtractor(allow=r'http://chuansongme.com/accounts/.+'),  follow=True, callback = 'parse_items'),
        Rule(LinkExtractor(allow=r'http://chuansongme.com/accounts\?start=\d+'),  follow=True, callback = 'parse_items'),
        Rule(LinkExtractor(allow=r'http://chuansongme.com/accounts/.+\?start=\d+'),  follow=True, callback = 'parse_items'),
        #Rule(LinkExtractor(allow=r'http://chuansongme.com/account/.+'), callback='parse_item'),
    )

    def parse_items(self, response):
        res = []
        
        nodes = response.xpath(r'//a[@class="user"]')
        
        for node in nodes:
            item = ChuansongmeItem()
            uri = node.xpath('.//@href').extract()
            if uri:
                userid = uri[0].split('/')[2]
                item['userid'] = userid
            else:
                return
            
            text = node.xpath(r'.//text()').extract()
            if text:
                nickname = text[0]
                item['nickname'] = nickname
            else:
                item['nickname'] = None
                
            item['gongneng'] = None
            res.append(item)
            
        return res
        
        
    def parse_item(self, response):
        i = ChuansongmeItem()
        
        childs = response.xpath('//*[@id="ld_E6G600_305"]/text()').extract()
        log.msg("userid" + repr(childs), level = log.DEBUG)
        
        if len(childs) == 1: 
            i['userid'] = self.__post_process_userid(childs[0])
        else:
            return
        
        nodes = response.xpath(r'//*[@id="ld_XT398O_291"]/text()').extract()
        log.msg("nickname" + repr(nodes), level = log.DEBUG)
        
        if len(nodes) == 1:
            i['nickname'] = nodes[0]
        else:
            i['nickname'] = None
        
        nodes = response.xpath('//*[@id="__w2_qcGcPvc_text_snip_content"]/text()').extract()
        log.msg("gongneng" + repr(nodes), level = log.DEBUG)
        
        if len(nodes) == 1:
            i['gongneng'] = nodes[0]
        else:
            i['gongneng'] = None
            
        return i

    def __post_process_userid(self, st):
        log.msg("\"%s\"" %st)
        log.msg("\"%s\"" %type(st))
    
        st = st.strip()
        if st.startswith('微信ID'.decode('utf-8')):
            return st.split(':')[1]
        else:
            return None