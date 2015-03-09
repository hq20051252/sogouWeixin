#!/usr/bin/python 
#-*- coding:utf-8-*-
#DATE: 2014/12/14
#AUTHOR: heqi
#EMAIL: heqi3@umessage.com.cn
#Describsion: 


from scrapy import log
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from sogouWeixin.items import SogouweixinItem
from sogouWeixin.settings import QUERYFILE

from fieldxpath import itemxpath, field_xpath

import re
import json
import urllib
import urlparse

class WeixinIDSpider(CrawlSpider):

    subn = re.compile("<em>|<!--red_beg-->|<!--red_end-->|</em>|<h3>|</h3>")
    name = "sogouWeixin"
    allowed_domains = ["sogou.com"]
    start_urls = ["http://weixin.sogou.com/weixin?"]
    rules = [
             Rule(LinkExtractor(allow=(r'http://weixin.sogou.com/weixin\?num=\d+&query=.*&tsn=\d+&type=1.*')), callback = "parse_items", follow = True),
             #Rule(LinkExtractor(allow=(r'/gzh\?openid=[_a-zA-Z0-9]+',)),callback = "parse_items", follow = True)
             ]

    # 这几个节点的模式相同, 要判断属于哪一个字段, 只能从内容上判断.
    def parse_type(self, node):
        #r'./span[@class="sp-tit"]/text()'
        ty = {
              "功能介绍：":("gongneng",),
              "认证：":("renzhenginfo",),
              "最近文章：":("latestarticle", "latestarticleuri", "latestupdatetime", "serid")
              }
        st = node.xpath(r'./span[@class="sp-tit"]/text()')[0].extract()
        return ty.get(st.encode('utf-8'), [])

    # 用于
    def get_all(self, response):
        sel = Selector(response)
        items = sel.xpath(itemxpath)
        return items
    
    def get_nickname(self, node):
        if not node:
            return None 
        html_part = node.extract()

        if not html_part:
            return None

        nickname, count = self.subn.subn("", html_part)

        return nickname if nickname else None
    
    def get_userid(self, node):
        if not node:
            return None
        
        st = node.extract()
        if st.startswith("微信号".decode('utf-8')):
            return st.split("：".decode('utf-8'))[1]
        else:
            return None
    
    def get_serid(self, node):
        if not node:
            return None
        
        uri = self.get_latestarticleuri(node)
        
        if uri:
            serid = urlparse.parse_qs(urlparse.urlsplit(uri).query)['__biz'][0]
            return serid
        
        return None
    
    def get_renzhenginfo(self, node):
        log.msg("inside get_renzhenginfo.", level = log.DEBUG)
        if node:
            html_part = node.extract()
            if not html_part:
                return None

            renzhenginfo, count = self.subn.subn("", html_part)

            return renzhenginfo
        
        return None
    
    def get_gongneng(self, node):
        if node:
            html_part = node.extract()
            if not html_part:
                return None

            gongneng, count = self.subn.subn("", html_part)

            return gongneng

        return None
    
    def get_latestarticle(self, node):
        log.msg("inside get_latestarticle.", level = log.DEBUG)
        if node:
            html_part = node.extract()
            if not html_part:
                return None

            article, count = self.subn.subn("", html_part)
            return article
        
        return None
    
    def get_latestupdatetime(self, node):
        if node:
            st = str(node.extract())
            startpos = st.find('write(\'')
            endpos = st.rfind('\')')
            t = st[startpos + 7:endpos]
            
            if t.isdigit():
                return t
        
        return None        
    
    def get_latestarticleuri(self, node):
        if not node:
            return None
        
        uri = node.extract()
        return uri

    def get_sogougzh(self, node):
        if not node:
            return None

        uri = node.extract()
        return uri

    def get_logo(self, node):
        if not node:
            return None

        uri = node.extract()
        return uri

    def get_qrcode(self, node):
        if not node:
            return None

        uri = node.extract()
        return uri

    # 每个字段对应的处理函数.
    field_action = {
                "sogougzh" : get_sogougzh,
                "logo"     : get_logo,
                "qrcode"   : get_qrcode,
                "nickname" : get_nickname,
                "userid"   : get_userid,
                "serid"    : get_serid,
                "gongneng" : get_gongneng,
                "renzhenginfo" : get_renzhenginfo,
                "latestarticle" : get_latestarticle,
                "latestupdatetime" : get_latestupdatetime,
                "latestarticleuri" : get_latestarticleuri,
                ("serid", 
                 "gongneng", 
                 "renzhengInfo", 
                 "latestarticle", 
                 "latestarticleuri", 
                 "latestupdatetime"): parse_type
            }    
    
    def parse_items(self,response):
        items = self.get_all(response)
        
        res = []
        for item in items:
            info = SogouweixinItem()
            for field in field_xpath.keys():
                if isinstance(field, tuple):
                    rootpath, childpath = field_xpath[field]
                    nodes = item.xpath(rootpath)
                    for node in nodes: 
                        nodetypes = self.parse_type(node)
                        log.msg("processing " + repr(nodetypes), level = log.DEBUG)
                        for key in nodetypes:
                            log.msg("processing " + key, level = log.DEBUG)
                            log.msg("child xpath " + repr(childpath), level = log.DEBUG)
                            log.msg( key + " xpath " + repr(childpath[key]), level = log.DEBUG)
                            vnode = node.xpath(childpath[key])
                            log.msg(key + " node " + repr(vnode), level = log.DEBUG)
                            if not vnode:
                                continue
                            else:
                                vnode = vnode[0]
                            value = self.field_action.get(key)(self, vnode)
                            log.msg(key + ":" + repr(value), level = log.DEBUG)
                            info[key] = value
                else:
                    node = item.xpath(field_xpath[field])
                    if not node:
                        pass
                    else:
                        node = node[0]
                        value = self.field_action.get(field)(self, node)
                        log.msg(field + ":" + repr(value), level = log.DEBUG)
                        info[field] = value
            res.append(info)
            
        return res
    
    def start_requests(self):
        queryfile = QUERYFILE
        fd = open(queryfile, 'rb')
        interface = self.start_urls[0]
        for line in fd.xreadlines():
            d = json.loads(line)
            nickname = d.get("nickname")
            if not nickname:
                continue
            # 查询词是从帐号昵称做k-gram切分得到.
            # 使用K-gram方式来得到查询词, 当k大于4时,效果不好.
            length = len(nickname) if len(nickname) < 4 else 4

            for k in range(1, length):
                for begin in range(0, length - k + 1):
                    option = [('num', 100), ("type",1), ("query",d["nickname"][begin:begin + k].encode('utf-8')), ("tsn", 0)]
                    option = urllib.urlencode(option)
                    url = interface + option
                    log.msg("*************************CRAWL URL****************************\n" + url, level = log.INFO)
                    yield self.make_requests_from_url(url)
    