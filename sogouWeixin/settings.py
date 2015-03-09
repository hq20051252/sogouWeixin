# -*- coding: utf-8 -*-

# Scrapy settings for sogouWeixin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sogouWeixin'

SPIDER_MODULES = ['sogouWeixin.spiders']
NEWSPIDER_MODULE = 'sogouWeixin.spiders'

DOWNLOADER_MIDDLEWARES = {
    'sogouWeixin.middleware.CustomHttpProxyMiddleware': 543,
    'sogouWeixin.middleware.CustomUserAgentMiddleware': 545,
}

ITEM_PIPELINES = {'sogouWeixin.pipelines.SogouweixinPipeline':200}
LOG_LEVEL = "DEBUG"
#LOG_LEVEL = "INFO"
LOG_FILE = "/home/hadoop/workspace/work/sogouWeixin/logs/scrapy.log"

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = False

DATAHOME = "/home/hadoop/workspace/work/sogouWeixin/data/"
QUERYFILE = "/home/hadoop/workspace/work/sogouWeixin/data/queryfile.txt"
HISTORYPAGE_FILE = "/home/hadoop/workspace/work/sogouWeixin/data/historypage_file.txt"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sogouWeixin (+http://www.yourdomain.com)'
REDIRECT_ENABLED = False