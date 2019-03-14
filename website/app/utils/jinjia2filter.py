# 将mongo中的文件名转换为预览文件名
def format_filename(filename):
    newfile_name = filename.split('.')[0]+'_260_534.'+filename.split('.')[1]
    return newfile_name

def format_filenameurl(filename):
    name = filename.split('.')[0]
    return name