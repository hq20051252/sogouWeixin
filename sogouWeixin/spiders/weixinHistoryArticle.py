# -*- coding: utf-8 -*-
import re
import json
import scrapy
import urlparse
import urllib

from scrapy import log
from sogouWeixin.settings import HISTORYPAGE_FILE
from sogouWeixin.items import SogouArticleweixinItem as OutputItem


class SogouarticleSpider(scrapy.Spider):
    name = "weixinhistoryarticle"
    allowed_domains = ["sogou.com"]
    start_urls = (
        'http://weixin.sogou.com/gzhjs?',
    )

    # 用于取得文章所在块的所有node
    def get_all(self, response):
        data = response.body
        start = data.find('({')
        end = data.find('})')
        data = data[start + 1: end + 1]

        res = json.loads(data)

        totalitems = res['totalItems']
        totalpages = res['totalPages']
        page = res['page']
        items = res['items']

        if len(items) > 0:
            openid = self.get_sogougzh(items[0])
        else:
            openid = ""

        return totalitems, totalpages, page, items, openid

    # 分析文章链接中的参数
    def _get_param(self, node, param):
        if not node:
            return None

        uri = self.get_articleuri(node)

        if uri:
            log.msg("Article URL is : %s. \n Get %s ." % (uri, param))
            try:
                value = urlparse.parse_qs(urlparse.urlsplit(uri).query)[param][0]
            except KeyError, e:
                log.msg(e.message, level=log.ERROR)
                value = None
            return value

        return None

    def get_serid(self, node):
        return self._get_param(node, "__biz")

    def get_mid(self, node):
        names = ("mid", "appmsgid")

        for key in names:
            value = self._get_param(node, key)
            if value:
                return value

        return value

    def get_idx(self, node):
        names = ("idx", "itemidx")

        for key in names:
            value = self._get_param(node, key)
            if value:
                return value

        return value

    def get_sn(self, node):
        names = ("sn", "sign")

        for key in names:
            value = self._get_param(node, key)
            if value:
                return value

        return value

    def get_title(self, node):
        pattern = r'<title><!\[CDATA\[(.*)\]\]><\/title>'
        return self._re_extract(node, pattern)

    def get_summary(self, node):
        pattern = r'<content168><!\[CDATA\[(.*)\]\]><\/content168>'
        return self._re_extract(node, pattern)

    def get_cover(self, node):
        pattern = r'<imglink><!\[CDATA\[(.*)\]\]><\/imglink>'
        return self._re_extract(node, pattern)

    def get_updatetime(self, node):
        pattern = r'<date><!\[CDATA\[(.*)\]\]><\/date>'
        return self._re_extract(node, pattern)

    @staticmethod
    def _re_extract(node, pattern):
        log.msg("Content is : %s" % node, level=log.DEBUG)
        log.msg("Pattern is : %s" % pattern, level=log.DEBUG)
        rep = re.compile(pattern)
        if not node:
            return None

        m = rep.search(node)
        return m.group(1) if m else None


    def get_articleuri(self, node):
        pattern = r'<url><!\[CDATA\[(.*)\]\]><\/url>'
        return self._re_extract(node, pattern)

    def get_docid(self, node):
        pattern = r'<docid>([a-z0-9-]+)<\/docid>'
        return self._re_extract(node, pattern)

    def get_classid(self, node):
        pattern = r'<classid>([0-9]+)<\/classid>'
        return self._re_extract(node, pattern)

    def get_headimage(self, node):
        pattern = r'<headimage><!\[CDATA\[(.*)\]\]><\/headimage>'
        return self._re_extract(node, pattern)

    def get_nickname(self, node):
        pattern = r'<sourcename><!\[CDATA\[(.*)\]\]><\/sourcename>'
        return self._re_extract(node, pattern)

    def get_sogougzh(self, node):
        pattern = r'<openid><!\[CDATA\[(.*)\]\]><\/openid>'
        return self._re_extract(node, pattern)

    def get_lastmodified(self, node):
        pattern = r'<lastModified>(.*)<\/lastModified>'
        return self._re_extract(node, pattern)


    field_action = {
        "docid": get_docid,
        "classid": get_classid,
        "headimage": get_headimage,
        "sogougzh": get_sogougzh,
        "nickname": get_nickname,
        "cover": get_cover,
        "title": get_title,
        "serid": get_serid,
        "articleuri": get_articleuri,
        "summary": get_summary,
        "mid": get_mid,
        "idx": get_idx,
        "sn": get_sn,
        "lastmodified": get_lastmodified,
        "updatetime": get_updatetime}


    def parse(self, response):
        totalitems, totalpages, page, items, openid = self.get_all(response)

        # 还有页面要抓. 重新生成一个请求.
        if page < totalpages and openid:
            # 构造请求, 使用迭代器的形式逐个返回request对象.
            interface = self.start_urls[0]
            option = [("cb", "sogou.weixin.gzhcb"), ("openid", openid), ("page", page + 1), ('num', 100)]
            option = urllib.urlencode(option)
            url = interface + option
            log.msg("Get the user:%s ,  %s page. The page is %s." %(openid, page + 1, url), level=log.INFO)
            return self.make_requests_from_url(url)

        res = []
        for item in items:
            info = OutputItem()
            for field, action in self.field_action.items():
                if not item:
                    pass
                else:
                    value = action(self, item)
                    log.msg(field + ":" + repr(value), level=log.DEBUG)
                    info[field] = value
            res.append(info)

        return res

    def start_requests(self):
        interface = self.start_urls[0]
        historypage_file = HISTORYPAGE_FILE
        fd = open(historypage_file, 'rb')

        progress = 0
        for line in fd.xreadlines():
            # 获取公众号的serid, 加密后的id.拿不到就跳过这一行.
            try:
                user = json.loads(line)
                historypage = user.get('sogougzh',"")
                openid = historypage.split('openid=')[1]

                if not historypage:
                    continue
                elif len(historypage) > 100:
                    continue
                else:
                    pass
            except ValueError, e:
                log.msg("This is a invalid json serielizer json object. \n %" %line, level = log.INFO)
                continue

            # 构造请求, 使用迭代器的形式逐个返回request对象.
            option = [("cb", "sogou.weixin.gzhcb"), ("openid", openid), ("page", 1), ('num', 100)]
            option = urllib.urlencode(option)
            url = interface + option
            progress += 1
            log.msg("Get the %s user's page." %progress, level = log.INFO)
            yield self.make_requests_from_url(url)
