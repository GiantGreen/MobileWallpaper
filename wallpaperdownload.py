#对mongo中urlinfo集合中的地址,图片下载
import requests
import redis
import os
from loguru import logger
from mongohandle import myMongo
from lxml import etree

#设置图片下载日志格式
logger.add("{time:YYYY-MM-DD}_pagedownload.log", rotation="12:00",
                   format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

BASEDIR = '/home/leimin/projects/myproject/MobileWallPaper/website/app/static'

class wallpaperDownload:

    def __init__(self):

        # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
        pool = redis.ConnectionPool(host='localhost', port=6379,decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.session = requests.Session()


    def downloadImage(self,url,filename):

        newfile = BASEDIR+'/download/'+filename
        if os.path.exists(newfile):
            logger.debug('file:{0} its already exists no need download again'.format(newfile))
        else:
            response = requests.get(url, stream=True)
            # 这里打开一个空的png文件，相当于创建一个空的txt文件,wb表示写文件
            logger.debug('file:{0} ready to download'.format(newfile))
            with open(newfile, 'wb') as file:
                # 每128个流遍历一次
                for data in response.iter_content(128):
                    # 把流写入到文件，这个文件最后写入完成就是，selenium.png
                    file.write(data)  # data相当于一块一块数据写入到我们的图片文件中

    #从mongo中获取需要下载的url列表,在redis中检查如果已存在则表明下载过,如果不存在则下载并更新到redis
    def getDownloadPage(self):
        mymongo = myMongo()
        urls  = mymongo.queryAllUrl()
        for url in urls:
            redisResult = self.r.get(url["address"])
            if redisResult == None:
                logger.info('address:{0} not in redis,needed to download'.format(url["address"]))
                r = self.session.get(url["address"])
                html = etree.HTML(r.text)
                try:
                    imgurl = html.xpath('/html/body/div[1]/div[2]/div[3]/a[2]/@href')[0]
                    imgurl_download = html.xpath('/html/body/div[1]/div[2]/div[3]/a[2]/@download')[0]
                except Exception as e:
                    imgurl = html.xpath('/html/body/div[1]/div[2]/div[3]/a/@href')[0]
                    imgurl_download = html.xpath('/html/body/div[1]/div[2]/div[3]/a/@download')[0]
                imgtags = html.xpath('/html/body/div[1]/div[2]/div[1]/p[1]/a/text()')
                image_name = (imgurl.split('/')[-1]).split('.')[0]+imgurl_download+'.'+(imgurl.split('/')[-1]).split('.')[1]
                files = mymongo.queryFile(image_name)

                self.downloadImage(imgurl,image_name)

                #将下载的文件名跟标签建立映射存入mongo
                if imgtags.__len__() == 0:
                    tags = ''
                else:
                    tags = imgtags[0]

                if(len(files) == 0):
                    logger.info('insert file:{0},tags:{1} to mongo'.format(image_name,tags))
                    mymongo.insertFile(image_name,tags)
                else:
                    logger.info('file:{0} already exists'.format(image_name))

                #将下载过的链接存入redis,10小时内不再下载
                self.r.set(url["address"],1,ex=36000)
            else:
                logger.debug("url:{0} its already in redis 10 hours will not request again".format(url["address"]))





if __name__ == '__main__':
    d1 = wallpaperDownload()
    d1.getDownloadPage()