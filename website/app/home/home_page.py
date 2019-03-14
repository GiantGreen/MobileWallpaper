from . import home
from ..utils.mongohandle import mongoDB
from flask import render_template,request
import imageio

def queryImgSize(file):
    basedir = '/home/leimin/projects/myproject/MobileWallPaper/website/app/static/download/'
    height, width, channels = imageio.imread(basedir+file).shape
    return height,width

@home.route('/',methods=['GET','POST'])
def index():
    mymongo = mongoDB()
    page = request.args.get('page')
    maxpage = int(mymongo.queryFileCount() / 30 + 1)

    #如果page为None则设置page为1,如果大于maxpage则设置为maxpage
    if page == None:
        page = 1

    if int(page) > maxpage:
        page = maxpage

    #获取当前标签,传递给模板展示
    tags = mymongo.queryTagDisinct()
    temptags = []
    for tag in tags:
        newtag = tag.split("，")
        if len(newtag) > 1:
            for ntag in newtag:
                temptags.append(ntag)
        else:
            temptags.append(tag)
    newtags = list(set(temptags))
    newtags.sort(reverse=True)
    #首页默认为所有标签按文件进行排序
    files = mymongo.queryAllFile(int(page))
    return render_template('index.html',newtags=newtags,files=files,maxpage=maxpage,page=int(page))

#点击标签时显示的页面
@home.route('/<tagname>',methods=['GET','POST'])
def showtag(tagname):
    mymongo = mongoDB()
    page = request.args.get('page')
    maxpage = int(mymongo.queryTagFileCount(tagname) / 30 + 1)

    # 如果page为None则设置page为1,如果大于maxpage则设置为maxpage
    if page == None:
        page = 1

    if int(page) > maxpage:
        page = maxpage

    # 获取当前标签,传递给模板展示
    tags = mymongo.queryTagDisinct()
    temptags = []
    for tag in tags:
        newtag = tag.split("，")
        if len(newtag) > 1:
            for ntag in newtag:
                temptags.append(ntag)
        else:
            temptags.append(tag)
    newtags = list(set(temptags))
    newtags.sort(reverse=True)
    # 首页默认为所有标签按文件进行排序
    files = mymongo.queryTagFile(tagname,int(page))
    return render_template('index.html', newtags=newtags, files=files, maxpage=maxpage, page=int(page),tagname=tagname)

#点击图片时显示的页面
@home.route('/<tagname>/<filename>')
def showpic(tagname,filename):
    mymongo = mongoDB()

    # 获取当前标签,传递给模板展示
    tags = mymongo.queryTagDisinct()
    temptags = []
    for tag in tags:
        newtag = tag.split("，")
        if len(newtag) > 1:
            for ntag in newtag:
                temptags.append(ntag)
        else:
            temptags.append(tag)
    newtags = list(set(temptags))
    newtags.sort(reverse=True)

    files = mymongo.queryRealFile(filename)
    realfile = files[0]
    height, width = queryImgSize(realfile['filename'])
    return render_template('imgshow.html',newtags=newtags,tag=tagname,realfile=realfile,filename=filename,height=height,width=width)