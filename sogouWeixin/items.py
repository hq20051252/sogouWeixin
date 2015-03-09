# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SogouweixinItem(scrapy.Item):
    # define the fields for your item here like:
    # sogou中, 帐号的历史页面
    sogougzh = scrapy.Field()
    # 帐号的logo
    logo = scrapy.Field()
    # 帐号的二维码
    qrcode = scrapy.Field()
    # 帐号别名
    nickname = scrapy.Field()
    # 帐号
    userid = scrapy.Field()
    # 加密帐号
    serid = scrapy.Field()
    # 帐号宣传语
    gongneng = scrapy.Field()
    # 认证类型
    renzhenginfo = scrapy.Field()
    # 最近发表文章
    latestarticle = scrapy.Field()
    # 最近发表时间
    latestupdatetime = scrapy.Field()
    # 最近文章链接
    latestarticleuri = scrapy.Field()

class ArticleweixinItem(scrapy.Item):

    # sogou中, 帐号的历史页面
    sogougzh = scrapy.Field()
    # 加密帐号
    serid = scrapy.Field()
    # 帐号别名
    nickname = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章摘要
    summary = scrapy.Field()
    # 文章封面
    cover = scrapy.Field()
    # 文章发布时间
    updatetime = scrapy.Field()
    # 文章链接
    articleuri = scrapy.Field()
    # 文章期号
    mid = scrapy.Field()
    # 文章当期编号
    idx = scrapy.Field()
    # N\A
    sn  = scrapy.Field()

class SogouArticleweixinItem(scrapy.Item):

    # docid
    docid = scrapy.Field()
    # classid
    classid = scrapy.Field()
    # headimage
    headimage = scrapy.Field()
    # sogou中, 帐号的历史页面
    sogougzh = scrapy.Field()
    # 加密帐号
    serid = scrapy.Field()
    # 帐号别名
    nickname = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章摘要
    summary = scrapy.Field()
    # 文章封面
    cover = scrapy.Field()
    # 文章发布时间
    updatetime = scrapy.Field()
    # 文章修改时间
    lastmodified = scrapy.Field()
    # 文章链接
    articleuri = scrapy.Field()
    # 文章期号
    mid = scrapy.Field()
    # 文章当期编号
    idx = scrapy.Field()
    # N\A
    sn  = scrapy.Field()

class ChuansongmeItem(scrapy.Item):
    #nickname
    nickname = scrapy.Field()
    # 帐号
    userid = scrapy.Field()
    # 帐号宣传语
    gongneng = scrapy.Field()
