#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
Created on Dec 12, 2014

@author: hadoop
'''

itemxpath = r'//div[@class="main"]/div[@class="weixin-public"]/div/div[@class="results"]/div[@class="wx-rb wx-rb3"]'

# //*[@id="sogou_vr_11002301_box_0"]/div[2]/p[3]/span[2]/span/text()
# 表示信息所在节点的xpath.如果key是元组,表示信息在同一个节点下,value是一个列表,第一个值是共同节点的xpath, 
# 第二个值是信息在该节点下子节点的xpath, 是相对路径xpath, 由一个字典表示.
field_xpath = {
         # sogou公众号页面, 可以看到该公众号的历史文章.
         "sogougzh"           : r'./div[@class="txt-box"]/div[@class="s-p"]/a[@id="weixin_account"]/@href',
         "nickname"           : r'./div[@class="txt-box"]/div[@class="s-p"]/a[@id="weixin_account"]',
         "serid"             :  r'./div[@class="txt-box"]/h4/a/@href',
         "title"             : r'./div[@class="txt-box"]/h4/a',
         "cover"             : r'./div[@class="img_box2"]/a/img/@src',
         "articleuri"        : r'./div[@class="txt-box"]/h4/a/@href',
         "summary"           : r'./div[@class="txt-box"]/p[@id="sogou_vr_11002601_summary_0"]',
         "updatetime"         : r'./div[@class="txt-box"]/div[@class="s-p"]',
         "mid"                : r'./div[@class="txt-box"]/h4/a/@href',
         "idx"                : r'./div[@class="txt-box"]/h4/a/@href',
         "sn"                 : r'./div[@class="txt-box"]/h4/a/@href',
}