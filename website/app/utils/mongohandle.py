from pymongo import MongoClient

class mongoDB:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.wallpaper
        self.collection = self.db['fileinfo']
        self.tagcollection = self.db['taginfo']
        self.urlcollection = self.db['urlinfo']

    def queryTagDisinct(self):
        results = self.collection.find().distinct('tag')
        return results

    def queryFileCount(self):
        filecount = self.collection.find().count()
        return filecount

    def queryAllFile(self,page):
        if page == 1:
            results = list(self.collection.find().sort([("_id", -1)]).limit(30))
        else:
            results = list(self.collection.find().sort([("_id", -1)]).skip((page-1)*30).limit(30))
        return results

    def queryTagFileCount(self,tag):
        keyword = tag
        condition = {}
        query_data = {}
        condition['$regex'] = keyword
        query_data["tag"] = condition
        filecount = self.collection.find(query_data).count()
        return filecount

    def queryTagFile(self,tag,page):
        keyword = tag
        condition = {}
        query_data = {}
        condition['$regex'] = keyword
        query_data["tag"] = condition
        if page == 1:
            results = list(self.collection.find(query_data).sort([("_id", -1)]).limit(30))
        else:
            results = list(self.collection.find(query_data).sort([("_id", -1)]).skip((page-1)*30).limit(30))
        return results

    def queryRealFile(self,name):
        keyword = name
        condition = {}
        query_data = {}
        condition['$regex'] = keyword
        query_data["filename"] = condition
        results = list(self.collection.find(query_data))
        return results