from pymongo import MongoClient

class myMongo:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.wallpaper
        self.collection = self.db['fileinfo']
        self.tagcollection = self.db['taginfo']
        self.urlcollection = self.db['urlinfo']

    #根据图片名字查询图片是否存在数据库,存在则不插入,不存则插入
    def queryFile(self,filename):
        query_data = {"filename":filename}
        results = list(self.collection.find(query_data))
        return results

    #将文件名,标签信息录入数据库
    def insertFile(self,filename,tag):
        insert_data = {"filename":filename,"tag":tag}
        self.collection.insert_one(insert_data)

    def queryTag(self,tagname):
        query_data = {"tagname":tagname}
        results = list(self.tagcollection.find(query_data))
        return results

    def insertTag(self,tagname,url):
        insert_data = {"tagname":tagname,"url":url}
        self.tagcollection.insert_one(insert_data)

    def queryAllTag(self):
        results = list(self.tagcollection.find())
        return results

    #查询子页面
    def queryUrl(self,address):
        query_data = {"address":address}
        results = list(self.urlcollection.find(query_data))
        return results

    def queryAllUrl(self):
        results = list(self.urlcollection.find())
        return results

    #将子页面写入mongo 集合collection
    def insertUrl(self,address):
        insert_data = {"address":address}
        self.urlcollection.insert_one(insert_data)