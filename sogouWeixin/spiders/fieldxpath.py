#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
Created on Dec 12, 2014

@author: hadoop
'''

itemxpath = r'//div[@class="wrap"]/div[@class="wrapper"]/div[@class="main"]/div[@class="weixin-public"]/div[3]/div[@class="results mt7"]/div[@class="wx-rb bg-blue wx-rb_v1 _item"]'

# 表示同一节点下的一组信息的xpath
extxpath = {
          "serid"             : r'./span[@class="sp-txt"]/a',
          "gongneng"          : r'./span[@class="sp-txt"]',
          "renzhenginfo"      : r'./span[@class="sp-txt"]',
          "latestarticle"     : r'./span[@class="sp-txt"]/a/text()',
          "latestarticleuri"  : r'./span[@class="sp-txt"]/a/@href',
          "latestupdatetime"  : r'./span[@class="sp-txt"]/span'
            }
# //*[@id="sogou_vr_11002301_box_0"]/div[2]/p[3]/span[2]/span/text()
# 表示信息所在节点的xpath.如果key是元组,表示信息在同一个节点下,value是一个列表,第一个值是共同节点的xpath, 
# 第二个值是信息在该节点下子节点的xpath, 是相对路径xpath, 由一个字典表示.
field_xpath = {
         # sogou公众号页面, 可以看到该公众号的历史文章.
         "sogougzh"           : r'./@href',
         # 公众号的logo.
         "logo"               : r'./div[@class="img-box"]/img/@src',
         # 公众号的二维码.
         "qrcode"             : r'./div[@class="pos-ico"]/div[@class="pos-box"]/img/@src',
         "nickname"           : r'./div[@class="txt-box"]/h3',
         "userid"             :  r'./div[@class="txt-box"]/h4/span/text()',
         ("serid", 
          "gongneng", 
          "renzhengInfo", 
          "latestarticle", 
          "latestarticleuri", 
          "latestupdatetime") : [r'./div[@class="txt-box"]/p[*]', extxpath]
}