from flask import Flask
from .home import home as home_blueprint
from .utils.jinjia2filter import format_filename,format_filenameurl

def createApp():
    app = Flask(__name__)
    app.debug = True

    #注册过滤器
    app.jinja_env.filters['format_filename'] = format_filename
    app.jinja_env.filters['format_filenameurl'] = format_filenameurl

    #注册蓝本
    app.register_blueprint(home_blueprint)
    return app