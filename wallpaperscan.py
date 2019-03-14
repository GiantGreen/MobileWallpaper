# bizhi.bcoderss.com
# 功能：扫描bizhi.bcoderss.com全站,对新增的图片地址进行入库处理

import requests
from lxml import etree
from mongohandle import myMongo
from loguru import logger



class wallpaperScan:

    def __init__(self):
        self.BASEURL = 'http://bizhi.bcoderss.com'
        logger.add("{time:YYYY-MM-DD}_pagescan.log", rotation="12:00",
                   format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

    # 获取所有子标签URL,存入mongo
    def getAllTags(self):
        mytag = myMongo()
        session = requests.Session()
        r = session.get(self.BASEURL)
        html = etree.HTML(r.text)
        html_url_data = html.xpath('/html/body/div[1]//a/@href')
        html_tag_data = html.xpath('/html/body/div[1]//a/text()')

        # 如果标签集合不存在,则插入到集合
        for key, value in zip(html_tag_data, html_url_data):
            tags = mytag.queryTag(key)
            if len(tags) == 0:
                logger.info("tag:{0}-insert to taginfo".format(key))
                mytag.insertTag(key, value)
            else:
                logger.info("tag:{0}-already exists no needed insert to taginfo".format(key))

        newtags = mytag.queryAllTag()
        return newtags

    # 获取标签所有子页面地址写入mongo
    def getAllPages(self):
        alltags = self.getAllTags()
        mypage = myMongo()

        for tag in alltags:
            session = requests.Session()
            r = session.get(tag["url"])
            html = etree.HTML(r.text)

            # 获取分类的最后一页
            try:
                lastPage = html.xpath('//div[@id="pagination"]//a[@class="extend"]/@href')[0]
                pageCount = int(lastPage.split('/')[-2])
            except Exception as e:
                pageCount = 1
                logger.debug("page:{0} loading error error message:{1}".format(tag["url"], e.args))

            for i in range(1, pageCount + 1):

                # print(tag["url"]+"/page/{0}/".format(i))
                logger.info("current scan page：{0} at page {1} data.".format(tag["url"], i))
                if (i == 1):
                    r2 = session.get((tag["url"]))
                else:
                    r2 = session.get(tag["url"] + "/page/{0}/".format(i))
                html = etree.HTML(r2.text)

                baseRule = html.xpath('//*[@id="masonry"]//a')

                for base in baseRule:
                    pageURL = base.xpath('@href')[0]
                    #basetag = base.xpath('div/div[2]/span/text()')[0]
                    urls = mypage.queryUrl(pageURL)
                    if len(urls) == 0:
                        mypage.insertUrl(pageURL)
                        logger.info("page:{0} its inert to mongo".format(pageURL))
                    else:
                        logger.info("page:{0} its exists no needed to insert".format(pageURL))




if __name__ == '__main__':
    w1 = wallpaperScan()
    w1.getAllPages()
