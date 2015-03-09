# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import log
from settings import DATAHOME as _DATADIR

import json


class SogouweixinPipeline(object):
    
    def __init__(self):
        self.file = open(_DATADIR + 'article.j1', 'wb')
        
    def process_item(self, item, spider):
        try:
            line = json.dumps(dict(item)) + "\n"
        except Exception, e:
            log.err(e)
                
        self.file.write(line)
        return item
